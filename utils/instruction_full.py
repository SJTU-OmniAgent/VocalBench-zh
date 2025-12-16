import json 
import os 
import argparse
from funasr import AutoModel
import os
import json
import argparse
from pydub import AudioSegment
import warnings
from pypinyin import pinyin, Style
from per import calculate_per, text_normalization
from config import EMOTION2VEC_PLUS_LARGE

warnings.filterwarnings("ignore")
def find_emotion_id(text):
    id2emotion = ['生气', '高兴', '中性', '悲伤', '惊喜', 'unknown']
    text_lower = text.lower() 
    for i, emotion in enumerate(id2emotion):
        if emotion in text_lower:
            return i
    id2emotion = ['生气', '高兴', '中立', '伤心', '惊讶', 'unknown']
    text_lower = text.lower() 
    for i, emotion in enumerate(id2emotion):
        if emotion in text_lower:
            return i
    return id2emotion.index('unknown') 


def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio) 
    return duration

def count_words(text):
    return len(text.strip().split())

def gen_score(eval_json):
    wav_dir = eval_json.replace('result/instruction_following.json', 'wav/instruction_following')
    query_dir = '../audio/instruction_following'

    emotion_model = AutoModel(
          model=EMOTION2VEC_PLUS_LARGE,
          hub="ms",  
    )
    sucess = 0
    with open(eval_json, "r") as f:
        data = json.load(f)
    num = len(data)

    for instance in data:
        instance['Success'] = False
        index = int(instance['Qid'].split('-')[1])
        wav_file = os.path.join(wav_dir, instance['Qid'] + '.wav')
        if os.path.exists(wav_file):
          if index < 200 and instance['Correct']:
            gt = instance["Response"].lower()
            hyp = instance["Response_hyp"].lower()
            _, _, per = calculate_per(pinyin(text_normalization(gt), style=Style.TONE3), pinyin(text_normalization(hyp), style=Style.TONE3))
            if per < 0.05:
              if index < 50:
                  instance['Success'] = True
              elif index in range(50, 100):
                  emo_id = find_emotion_id(instance['Question'])
                  rec_result = emotion_model.generate(wav_file, output_dir="./save", granularity="utterance", extract_embedding=False)
                  prob_scores = rec_result[0]['scores'][emo_id]
                  if prob_scores > 0.5:
                    instance['Success'] = True
              elif index in range(100, 150):
                  all_len = count_words(instance["Question"])
                  valide_len = count_words(instance["Question"].split('。', 1)[1])
                  query_dur = get_audio_duration(os.path.join(query_dir, instance['Qid'].split('-')[1] + '.wav'))* valide_len / all_len
                  response_dur = get_audio_duration(wav_file) 
                  if "两倍" in instance["Question"].split('.', 1)[0].lower() or "快一倍" in instance["Question"].split('.', 1)[0].lower():
                    min_dur = query_dur * 0.25
                    max_dur = query_dur * 0.75
                  elif "一半" in instance["Question"].split('.', 1)[0].lower() or "慢一倍" in instance["Question"].split('.', 1)[0].lower():
                    min_dur = query_dur * 1.5
                    max_dur = query_dur * 2.5
                  else:
                    raise ValueError("Unknown time scale")
                  if min_dur < response_dur < max_dur:
                    instance['Success'] = True
              elif index in range(150, 200):
                  emo_id = find_emotion_id(instance['Question'])
                  rec_result = emotion_model.generate(wav_file, output_dir="./output", granularity="utterance", extract_embedding=False)
                  prob_scores = rec_result[0]['scores'][emo_id]
                  if prob_scores > 0.5:
                    all_len = count_words(instance["Question"])
                    valide_len = count_words(instance["Question"].split('。', 1)[1])
                    query_dur = get_audio_duration(os.path.join(query_dir, instance['Qid'].split('-')[1] + '.wav'))* valide_len / all_len
                    response_dur = get_audio_duration(wav_file) 
                    if "两倍" in instance["Question"].split('.', 1)[0].lower() or "快一倍" in instance["Question"].split('.', 1)[0].lower():
                      min_dur = query_dur * 0.25
                      max_dur = query_dur * 0.75
                    elif "一半" in instance["Question"].split('.', 1)[0].lower() or "慢一倍" in instance["Question"].split('.', 1)[0].lower():
                      min_dur = query_dur * 1.5
                      max_dur = query_dur * 2.5
                    else:
                      raise ValueError("Unknown time scale")
                    if min_dur < response_dur < max_dur:
                      instance['Success'] = True
          elif index>=200:
            instance['Success'] = instance["Correct"]
          sucess += instance['Success']

    print(f"Total_num: {num}; Following_num: {sucess}; Following rate: {sucess/num}.")
    
    output_json = eval_json.replace('.json', '_final.json')
    with open(output_json, 'w+', encoding = 'utf-8') as outf:
      json.dump(data, outf, ensure_ascii=False, indent = 4)

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_json", type=str)
    args = parser.parse_args()
    gen_score(args.eval_json)
