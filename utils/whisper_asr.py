import os
import json
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import soundfile as sf 
import json
import os 
import argparse
import sys
from config import WHISPER_LARGE_V3
sys.path.append("./whisper")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    WHISPER_LARGE_V3, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(WHISPER_LARGE_V3)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

def whisper_asr_wav(wav_path: str):
  audio_file_path = wav_path
  audio_input, sample_rate = sf.read(audio_file_path)
  sample = {"raw": audio_input, "sampling_rate": sample_rate}

  result = pipe(sample)
  return result["text"]


def json_wer(input_json, output_json, audio_dir):
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]

    instances = []
    if os.path.exists(output_json):
        with open(output_json, 'r', encoding='utf-8') as infile:
            finished = json.load(infile)
        for instance in finished:
            instances.append(instance)

    
    index = len(instances)
    print(f"Already Finished: {index}")
    for instance in data[len(instances):]:
        qid = instance['Qid']
        response_wav = os.path.join(audio_dir, f"{qid}.wav")
        assert os.path.exists(response_wav)
        hyp_r = whisper_asr_wav(response_wav)
        instances.append({
            'Qid': instance['Qid'],
            'Response': instance['Response'],
            'Response_hyp': hyp_r
        })

        with open(output_json, 'w+', encoding='utf-8') as outfile:
            json.dump(instances, outfile, ensure_ascii=False, indent=4)
        index += 1
        print(f"Finished: {index}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Whisper ASR zh')
    parser.add_argument('--input_json', type=str)
    parser.add_argument('--output_json', type=str)
    parser.add_argument('--audio_dir', type=str)
    args = parser.parse_args()
    json_wer(args.input_json, args.output_json, args.audio_dir)
