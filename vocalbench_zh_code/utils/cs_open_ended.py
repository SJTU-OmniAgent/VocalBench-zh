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

def qwenmax_eval_relevance(question, ans, response, qwenmax):
    prompt = f'''
你是一个专业的语言模型评估助手。你的任务是根据用户提出的问题和模型生成的回答，判断该回答是否正确理解了问题的语义，是否满足问题的要求。

评分标准
5分：完全正确。模型完全正确的理解了用户的问题内容，并有针对性的做出回答。
4分：主旨正确。模型的理解主体上符合问题的语义，回复主旨上符合问题的要求，但少量关键词理解有偏差。
3分：部分错误。模型理解了用户问题的部分关键词，但误解或遗漏了重要语义，导致回应偏离原意。
2分：明显错误。模型仅捕捉到表面词汇，未能理解核心语义或关键逻辑，回应基于错误理解。
1分：完全错误。模型完全没有理解用户的问题内容，回答与问题毫无关联。

输出格式
请简要解释您的评估，并在方括号中填写最终得分。示例：
模型理解了用户的部分意图，但对提问中的“cyber attacks”理解有误，答案偏离。得分：[3]

注意：只考虑模型回答与问题的相关程度，不考虑回复的用词、文采等语义质量。

问题：{question}
参考回答：{ans}
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

def qwenmax_eval_semantic(question, ans, response, qwenmax):
    prompt = f'''
你是一个专业的语言模型评估助手。你的任务是根据用户提出的问题和模型生成的回答，评估模型回复的语义质量，以及回复中的中英文使用是否合理。

评分标准
5分：优秀。模型回答精准、完整、自然、逻辑清晰，对于中文表达困难的部分合理使用英文进行回复。
4分：良好。回答大部分正确，有轻微信息遗漏或冗余，中英文使用较为合理。
3分：一般。模型回答部分正确，但存在明显遗漏或表达模糊，中英文表述不自然。
2分：较差。模型回答存在显著偏差、遗漏，语句不通顺，中英文使用混乱，语言生硬不自然。
1分：差。模型回答错误或回避问题，中英文使用混乱，语言文字使用极不合理。

输出格式
请简要解释您的评估，并在方括号中填写最终得分。示例：
模型回答大部分准确，但部分英文使用不自然，与日常表达存在差异。得分：[4]

注意：如果模型完全使用中文回复且语义完整、准确，不应扣分。

问题：{question}
参考回答：{ans}
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


def qwenmax_eval_json(input_json, output_json):
    ref_json = '../json/cs_open_ended.json'
    with open(ref_json, "r") as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]

    instances = []
    relevance_score = 0
    relevance_num = 0
    semantic_score = 0

    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        relevance_score += instance['Relevance']
        semantic_score += instance['Semantic']
        relevance_num += instance['Relevance'] > 3
        instances.append(instance)

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      ans = ref[index]['Answer']
      response = instance['Response']
      relevance, re_explain =  qwenmax_eval_relevance(ref[index]['Question'], ans, response, qwenmax)
      semantic, se_explain = qwenmax_eval_semantic(ref[index]['Question'], ans, response, qwenmax)
      
      instances.append({
          'Qid': instance['Qid'],
          'Response': response,
          'Relevance': relevance,
          'Relevance Explain': re_explain,
          'Semantic': semantic,
          'Semantic Explain': se_explain
      })
      relevance_score += relevance
      semantic_score += semantic
      relevance_num += relevance > 3
      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
        
    print(f'Avg Relevance Score: {relevance_score/len(instances)}')
    print(f'Relevance Rate: {relevance_num/len(instances)}')
    print(f'Avg Semantic Score: {semantic_score/len(instances)}')

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
