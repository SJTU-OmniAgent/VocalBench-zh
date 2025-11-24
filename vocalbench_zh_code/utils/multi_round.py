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


def qwenmax_eval_with_ans(question, history, ans, response, qwenmax):
    context = ""
    for turn in history:
        if turn['from'] == 'user':
            context = context + f"User: {turn['value']}\n"
        elif turn['from'] == 'assistant':
            context = context + f"Model: {turn['value']}\n"
    prompt = f'''
你是一个客观、严谨的语音问答评估助手。接下来，我将提供以下四项内容：

历史：用户与模型对话的历史。
问题：一个中文问题，在用户与模型完成历史对话后由用户提出。
正确答案：该问题对应的正确回答。
模型回答：模型针对该问题实际生成的回答。
请你根据以下要求进行分析与评估：

判断“模型回答”所包含的结果与正确答案是否一致。如果模型回答没有给出明确的结果或与问题无关，记为错误。如果模型回答包含了正确答案，记为正确。
注意：请忽略同音错误，如题目中的“小亮”和“晓亮”。如果模型回答为正确答案的同音内容，同样视为正确。
输出格式：正确/错误 [简单解释]
示例：正确 模型给出了明确的答案，并且与正确答案一致。

历史：{context}
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


def qwenmax_eval_json(input_json, output_json):
    ref_json = '../json/multi_round.json'
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
        correct_num += instance['Correct']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      history = ref[index]['Context']
      ans = ref[index]['Answer']
      response = instance['Response']
      
      
      correct, explain = qwenmax_eval_with_ans(ref[index]['Question'], history, ans, response, qwenmax)
      correct_num += correct
      
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Correct': correct,
          'Explain': explain
      })

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
    print(f"正确率为：{correct_num/len(instances)*100}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)