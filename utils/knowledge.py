import json
import sys
import json 
import random 
import os 
import requests
import argparse
import random
import time
from pypinyin import pinyin, Style
from per import calculate_per, text_normalization
from config import keys, Qwen_Max

random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")

def qwenmax_eval(question, ans, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的问答评估助手。接下来，我将提供以下三项内容：

问题：一个中文问题。
答案：该问题对应的正确回答。
模型回答：模型针对该问题实际生成的回答。
请你根据以下要求进行分析与评估：

判断“模型回答”与答案是否一致。如果模型回答是答案的别称，也记为正确。
输出格式：正确/错误 [简单解释]
示例：正确 模型回答与中文答案语义一致。

问题：{question}
答案：{ans}
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

def qwenmax_eval_json(input_json, output_json):
    if 'chinese' in input_json.lower():
        ref_json = '../json/chinese_knowledge.json'
    elif 'foreign' in input_json.lower():
        ref_json = '../json/foreign_knowledge.json'
    elif 'general' in input_json.lower():
        ref_json = '../json/general_knowledge.json'
    else:
        raise NotImplementedError

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
        if instance['Correct']:
          correct_num += 1

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      ans = ref[index]['Answer']
      response = instance['Response']
      response_hyp = instance['Response_hyp']
      _, _, per = calculate_per(pinyin(text_normalization(response), style=Style.TONE3), pinyin(text_normalization(response_hyp), style=Style.TONE3))
      if ans in response:
        instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Correct': True,
          'Explain': f"答案位于回复中：{ans}",
          'PER': per
        })
        correct_num += 1
      else:
        correct, explain = qwenmax_eval(ref[index]['Question'], ans, response, qwenmax)
        instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Correct': correct,
          'Explain': explain,
          'PER': per
        })
        correct_num += correct
      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
    
    print(f"正确率为：{correct_num/len(instances)*100}")



if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
