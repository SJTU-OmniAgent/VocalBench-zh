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


def qwenmax_eval_emotion_semantic(question, response, qwenmax):
    prompt = f'''
你是一位模型回复共情评估员。您将收到一个包含清晰情感内容的用户问题，问题背后的情感类型，以及模型生成的回复。你的任务是评估模型对用户情绪的理解、感知和共情能力，以及是否提供了适当的情感支持或积极暗示。

评分标准
5分：优秀。回复充分理解用户的情绪状态，并带有清晰的同理心，在保持真实和尊重的同时，提供了周到、支持的反馈，用户很可能对该回复满意。
4分：良好。回复能够识别用户的情绪，并提供适当的支持或鼓励。回复的深度或语气可能略有不足，但仍然具有情商。
3分：中等。回复试图体谅用户的感受，但表达方式略显泛泛或流于表面。回复可能缺乏深度或遗漏了微妙的情感线索，但仍能传达基本的同理心。
2分：差。回复对情感内容的理解有限。它可能过于公式化，或未能提供有意义的情感支持。语气可能显得不恰当或冷漠。
1分：差。回复完全未能识别或处理情感背景。它可能显得冷淡、无关紧要，用户很可能对该回复不满。

附加说明
关注情感共鸣和语气，而非语法或用词，除非它们严重影响理解。考虑模型是否带入了用户的感受，并提供了用户乐于得到的情感价值。


输出格式
简要说明您的评估，然后在方括号中填写最终分数。请使用以下格式：
回复展现了对用户焦虑的真诚理解，并提供了令人安心的保证，尽管其中一句话感觉略显泛泛。得分：[4]

问题：{question}
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
    ref_json = '../json/emotion.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    
    instances = []
    total_score = 0
    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        instances.append(instance)
        total_score += instance['Semantic_score']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      response = instance['Response']
      score, explain = qwenmax_eval_emotion_semantic(ref[index]['Question'], response, qwenmax)
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Semantic_score': score,
          'Explain': explain
      })
      total_score += score

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
    print(f"平均分数为：{total_score/len(instances)}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
