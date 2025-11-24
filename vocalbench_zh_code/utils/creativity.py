import json
import sys
import json 
import random 
import os 
import re
import argparse
import random
import time
from config import keys, Qwen_Max

random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")

def read_prompt(category):
    filepath = os.path.join("../prompt/creativity", f"{category}.txt") 
    with open(filepath, 'r') as file:
        return file.read()


def qwenmax_eval_creativity(prompt, qwenmax):
    for i in range(10):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        print(messages)
        text = qwenmax(messages)["text"]
        try:
            score = int(re.findall(r'\[([0-5])\]', text)[0])
            return score, text
        except:
            score = 1
    return score, text

def qwenmax_eval_json(input_json, output_json):
    set_to_id = {
        "Narratives": 0,
        "Argumentative": 1,
        "Descriptive": 2,
        "Role Play": 3,
        "Achient Poetry Appreciation": 4,
        "Achient Format Writing": 5,
        "Modern Poem Appreciation": 6,
        "Modern Poem Writing": 7
    }
    set_total = [0] * 8
    set_score = [0] * 8
    id_to_set = {v: k for k, v in set_to_id.items()}

    ref_json = '../json/creativity.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    
    instances = []
    overall_score = 0
    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        instances.append(instance)
        index = int(instance['Qid'].split('-')[1])
        set_id = set_to_id[ref[index]["Category"]]
        set_score[set_id] += instance['Score']
        set_total[set_id] += 1
        overall_score += instance['Score']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      query = ref[index]['Question']
      ans = ref[index]['Answer']
      category = ref[index]['Category'].lower().replace(' ','_')
      response = instance['Response']
      prompt_pre = read_prompt(category)
      if category in ['achient_poetry_appreciation', 'modern_poem_appreciation']:
        prompt =  f'''
{prompt_pre}
问题：{query}
参考答案：{ans}
模型回答：{response}
  '''
      else:
        prompt =  f'''
{prompt_pre}
问题：{query}
模型回答：{response}
  ''' 
      score, explain = qwenmax_eval_creativity(prompt, qwenmax)
      overall_score += score
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Score': score,
          'Explain': explain
      })
      set_id = set_to_id[ref[index]["Category"]]
      set_score[set_id] += score
      set_total[set_id] += 1

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
    print(f"平均得分为：{overall_score/len(instances)}")

    for i in range(len(set_total)):
        print("Set:", id_to_set[i], "  Total QA:", set_total[i], "  Score:", set_score[i]/set_total[i])
    print("平均分为：{:.3f}".format(overall_score/len(data)))


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
