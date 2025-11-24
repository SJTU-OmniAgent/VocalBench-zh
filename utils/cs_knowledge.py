import json
import sys
import json 
import random 
import os 
import argparse
import random
import time
from config import keys, Qwen_Max


random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")

def qwenmax_eval(question, ans_zh, ans_en, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的问答评估助手。接下来，我将提供以下四项内容：

问题：一个以中文为主的问题。
中文答案：该问题对应的正确中文回答。
英文答案：该问题对应的正确英文回答。
模型回答：模型针对该问题实际生成的回答。
请你根据以下要求进行分析与评估：

判断“模型回答”与中文或英文答案是否一致。如果模型回答是中文或英文答案的别称，也记为正确。
输出格式：正确/错误 [简单解释]
示例：正确 模型回答与中文答案语义一致。

问题：{question}
中文答案：{ans_zh}
英文答案：{ans_en}
模型回答：{response}
  ***
  '''
    for i in range(10):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        text = qwenmax(messages)["text"]
        if text.startswith("正确"):
          return True, text
        elif text.startswith("错误"):
          return False, text
    return False, text

def part_correct(ans_zh, response):
  assert '·' in ans_zh
  answer_parts = ans_zh.split('·')
  for part in answer_parts:
      if part.strip() in response:  
          return True
  return False

def qwenmax_eval_json(input_json, output_json):
    ref_json = '../json/cs_knowledge.json'
    with open(ref_json, "r") as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    
    correct_num = 0
    instances = []
    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        index = int(instance['Qid'].split('-')[1])
        instance['Category'] = ref[index]['Category']
        instances.append(instance)
        correct_num += instance['Correct']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      ans_zh = ref[index]['Answer_zh']
      ans_en = ref[index]['Answer_en']
      response = instance['Response']
      category = ref[index]['Category']
      if ans_zh in response or ans_en.lower() in response.lower() or ('·' in ans_zh and part_correct(ans_zh, response)):
        correct = True
        instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Category': category,
          'Correct': True,
          'Explain': f"答案位于回复中：{ans_zh}"
        })
      else:
        correct, explain = qwenmax_eval(ref[index]['Question'], ans_zh, ans_en, response, qwenmax)
        instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Category': category,
          'Correct': correct,
          'Explain': explain
        })
      correct_num += correct
      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)

    print(f"准确率: {correct_num/len(instances)}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
