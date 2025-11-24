import json
import sys
import json 
import random 
import os 
import re
import argparse
import random
import time
from collections import defaultdict
from config import keys, Qwen_Max


random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")

def qwenmax_eval_robust(question, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的问答评估助手。你将收到一个寻求实用建议或指导的问题，以及模型生成的回应。你的任务是根据建议的实用性、准确性、完整性和相关性，使用五分制对该回应进行评分。

评分标准
5分：优秀。回应提供了清晰、详细且高度相关的建议，直接切中问题核心。包含有价值的步骤或洞见，逻辑清晰、结构合理，能够全面满足用户的实际需求。
4分：良好。回应给出了有用且基本相关的建议，结构良好。可能存在轻微遗漏或细节不足，但整体内容有帮助、切题，具备较好的参考价值。
3分：中等。回应尝试提供建议，并涵盖了问题的基本方面，但缺乏深度、具体性或条理性。部分内容可能模糊或过于笼统，实用性受限。
2分：较差。建议不完整、偏离主题或过于模糊而难以应用。仅部分回应了问题，或在逻辑性与相关性方面存在明显缺失。
1分：差。回应未能提供任何有意义或可操作的建议，内容无关、误导性强，或明显未理解问题意图。

输出格式
请先简要说明评分理由，然后在方括号内给出最终得分。使用如下确切格式：
回应提供了清晰且可操作的步骤，直接回答了问题，仅有一条建议可进一步具体化。得分：[4]

问题：{question}
模型回答：{response}
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

def qwenmax_eval_json(input_json, output_json):
    ref_json = '../json/robust_clean.json'
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
        total_score += instance['Score']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[-1])
      response = instance['Response']
      score, explain = qwenmax_eval_robust(ref[index]['Question'], response, qwenmax)
      total_score += score
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Score': score,
          'Explain': explain
      })

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
def gen_score(output_json):
    assert output_json.endswith('robust.json')
    single_round_json = output_json.replace('robust.json', 'single_round.json')
    assert os.path.exists(single_round_json)
    with open(single_round_json, "r", encoding = 'utf-8') as f:
        sr_data = json.load(f)
    sr_score = 0
    sr_num = 0
    for instance in sr_data:
        if int(instance['Qid'].split('-')[-1])%2 == 0:
            sr_score += instance['Score']
            sr_num += 1
    clean_score = sr_score / sr_num

    with open(output_json, "r", encoding = 'utf-8') as f:
        data = json.load(f)
    
    set_scores = defaultdict(lambda: {'Score': []})
    for item in data:
        qid = item.get('Qid')
        score = item.get('Score')
        if not qid or score is None:
            continue  
        parts = qid.rsplit('-', 1)
        if len(parts) < 2:
            continue 
        set_name = parts[0]
        set_scores[set_name]['Score'].append(score)
    
    total_score = 0
    eval_sets = ['robust-background_noise-snr_-5', 'robust-white_noise-snr_-5', 'robust-reverberation-rt60_30', 'robust-packet_loss-dropping_0.70', 'robust-farfield-filter_400hz', 'robust-distortion-clipping_0.0001']
    for set_name in eval_sets:
        avg_score = sum(set_scores[set_name]['Score']) / len( set_scores[set_name]['Score']) if set_scores[set_name]['Score'] else 0
        pr = min(1, avg_score/clean_score)*2.5
        total_score = total_score + pr
    print(total_score/15 * 100)
    print(f"Overall Robust Score: {total_score}")



if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
    gen_score(args.output_json)
