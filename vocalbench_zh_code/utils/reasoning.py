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

def qwenmax_eval_with_ans(question, ans, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的问答评估助手。接下来，我将提供以下四项内容：

问题：一个中文问题，涉及简单的逻辑推理或数学运算。
正确答案：该问题对应的正确回答。
模型回答：模型针对该问题实际生成的回答。
请你根据以下要求进行分析与评估：

判断“模型回答”所包含的结果与正确答案是否一致。如果模型回答没有给出明确的结果或与问题无关，记为错误。如果模型回答包含了正确答案并加以适当的拓展，记为正确。
输出格式：正确/错误 [简单解释]
示例：正确 模型给出了明确的计算结果，并且与正确答案一致。

问题：{question}
正确答案：{ans}
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
        print(messages)
        text = qwenmax(messages)["text"]
        if text.startswith("正确"):
          return True, text
        elif text.startswith("错误"):
          return False, text
    return False, text

def qwenmax_eval_open_domain(question, ans, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的问答评估助手。接下来，我将提供以下四项内容：

问题：一个中文问题，涉及简单的逻辑推理。
参考答案：该问题对应的参考回答。
模型回答：模型针对该问题实际生成的回答。
请你根据以下要求进行分析与评估：

判分依据
5分：满分答案，模型的回答与参考答案一致，过程和结论均正确。
4分：答案正确，模型的回答与参考答案一致，但是过程简单；或者回答事实正确，但与参考答案角度不同。
3分：答案错误，答案结论错误，但推理过程中有部分正确成分；或结论正确，但关键推理步骤存在明显漏洞或错误。
2分：答案错误，且推理过程大部分不成立。
1分：答案错误，且推理过程混乱、无关或缺失。

输出格式
请简要说明您的评估，并在方括号中填写最终得分。请使用以下格式：

模型回答与参考答案一致，但是其步骤较为省略，思路略有跳跃。得分：[4]

问题：{question}
参考答案：{ans}
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
        print(messages)
        text = qwenmax(messages)["text"]
        try:
            score = int(re.findall(r'\[([0-5])\]', text)[0])
            return score, text
        except:
            score = 1
    return score, text

def part_correct(ans_zh, response):
  assert '·' in ans_zh
  answer_parts = ans_zh.split('·')
  for part in answer_parts:
      if part.strip() in response:  
          return True
  return False

def qwenmax_eval_json(input_json, output_json):
    set_to_id = {
        "Analogical": 0,
        "Causal": 1,
        "Common_sense": 2,
        "Conflict": 3,
        "Deductive/Inductive": 4,
        "Hypothesis": 5,
        "Story": 6,
        "Counter Proposition": 7,
        "Math": 8,
        "Graphological": 9,
        "Anachronisms": 10,
        "Movie Recommendation": 11,
        "Natural Language Inference": 12,
        "Reading Comprehension": 13,
        "Sequence Understanding": 14,
    }
    id_to_set = {v: k for k, v in set_to_id.items()}
    set_total = [0] * 15
    set_correct = [0] * 15

    ref_json = '../json/reasoning.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    
    instances = []
    correct_num = 0
    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        instances.append(instance)
        index = int(instance['Qid'].split('-')[1])
        set_id = set_to_id[ref[index]["Category"]]
        set_total[set_id] += 1
        correct_num += instance['Correct']
        set_correct[set_id] += instance['Correct']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      ans = ref[index]['Answer']
      response = instance['Response']
      ranges_with_ans = [(0, 150), (251, 341), (388, 463), (524, 793), (843, 851)]
      if any(lower <= index < upper for lower, upper in ranges_with_ans):
        correct, explain = qwenmax_eval_with_ans(ref[index]['Question'], ans, response, qwenmax)
        score = None
        correct_num += correct
      else:
        score, explain = qwenmax_eval_open_domain(ref[index]['Question'], ans, response, qwenmax)
        correct = (score > 3)
        correct_num += correct
      
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Correct': correct,
          'Score': score,
          'Explain': explain
      })
      set_id = set_to_id[ref[index]["Category"]]
      set_total[set_id] += 1
      set_correct[set_id] += correct


      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
    print(f"正确率为：{correct_num/len(instances)*100}")

    for i in range(len(set_to_id)):
        print("Set:", id_to_set[i], "  Total QA:", set_total[i], "  Accuracy:", set_correct[i]/set_total[i])
   
if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)

