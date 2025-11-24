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


def qwenmax_eval_instruction(question, instruct, response, qwenmax):
    prompt = f'''
你是一个客观、严谨的指令遵循评估助手。接下来，我将提供以下三项内容：

问题：一个中文问题，涉及用户指令。
模型回答：模型针对该问题实际生成的回答。
判断标准：判断模型是否正确遵循指令的标准。

返回模型是否正确遵循了用户指令。注意，仅依据判断标准评估模型是否遵循指令，不因事实错误、回复质量等其他因素影响评估。

输出格式
输出格式：正确/错误 [简单解释]
示例：正确 模型正确依据指令重复了用户的语言。

问题：{question}
模型回答：{response}
判断标准：{instruct}
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

def part_correct(ans_zh, response):
  assert '·' in ans_zh
  answer_parts = ans_zh.split('·')
  for part in answer_parts:
      if part.strip() in response:  
          return True
  return False

def qwenmax_eval_json(input_json, output_json):
    set_to_instruction = {
        "Plain repeat": '模型回复必须包含完整用户要求重复的内容。允许有极个别字词错误，和额外的解释。',
        "With emotion": '模型回复必须包含完整用户要求重复的内容。允许有极个别字词错误，和额外的解释。',
        "With speed": '模型回复必须包含完整用户要求重复的内容。允许有极个别字词错误，和额外的解释。',
        "With speed & emotion": '模型回复必须包含完整用户要求重复的内容。允许有极个别字词错误，和额外的解释。',
        "Num": '模型必须严格按用户指定数量进行列举。多于或少于指定数量均视为未遵循指令。',
        "Constrain": '模型在指定位置包含指定内容，且确保要求词汇出现次数达标。任一要求未满足即视为未遵循指令。',
        "Keywords": '模型必须包含所有指定关键词，且不出现任何排除关键词。任一不符即视为未遵循指令。',
        "Progressive": '模型必须严格按问题顺序逐项回答。顺序错误或遗漏任一问题均视为未遵循指令。',
        "Conditional": '要求模型根据先决问题的判断结果选择对应问题作答。选错问题或同时回答两个后续问题视为未遵循指令；先决问题错误所导致的后续问题选择错误，视为遵循指令。',
        "Topic change": '模型必须仅遵循用户最终更正后的指令。回应先前指令或回答更正前、后的指令均视为未遵循指令。',
        "Spoken format": '模型必须使用纯口语化文字回答。包含Latex代码、公式等结构化文本，均视为未遵循指令。',
        "Speaker tune": '模型必须根据指定受众身份或自身身份，使用恰当、合理的语言风格和口吻回答。语言不当、不合时宜或直叙均视为未遵循指令。',
        "Speaking style": '模型必须严格模仿指定人物的风格进行回复。风格不符或平铺直叙均视为未遵循指令。',
        "Instruction": '模型必须严格遵循用户指定的用词、结构及内容顺序。任何偏离或忽视均视为未遵循指令。',
        "Situation": '模型必须在回答中充分考虑并回应用户所述的所有具体情况，遗漏或明显冲突视为未遵循指令。',
        "Format": '模型必须严格遵循用户指定的格式，任何格式不符均视为未遵循指令。',
        "Mandarin specific": '模型必须严格使用指定的中文表达方式、文学体裁和参考中国的文化习俗，任何偏离均视为未遵循指令。'
    }
    ref_json = '../json/instruction.json'
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

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      if ref[index]["Sub-category"] is not None and ref[index]["Category"] != "Mandarin specific":
            instruct = set_to_instruction[ref[index]["Sub-category"]]
      else:
            instruct = set_to_instruction[ref[index]["Category"]]
      response = instance['Response']
      
      correct, explain = qwenmax_eval_instruction(ref[index]['Question'], instruct, response, qwenmax)
      correct_num += correct
      
      instances.append({
          'Qid': instance['Qid'],
          'Question': ref[index]['Question'],
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
