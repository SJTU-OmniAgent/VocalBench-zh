<div align="center">


# **📈VocalBench-zh: Decomposing and Benchmarking the Speech Conversational Abilities in Mandarin Context**
<!-- # 🎧VocalNet: Speech LLM with Multi-Token Prediction for Faster and High-Quality Generation -->
<!-- <strong>English | 
[Chinese](./README_zh.md)</strong> -->

</div>

<p align="center">
HuggingFace <a href="https://huggingface.co/datasets/VocalNet/VocalBench-zh">🤗</a> | Paper <a href="https://arxiv.org/abs/2511.08230">📖</a> 
</p>
<p align="center">
Shanghai Jiao Tong University</a>  |  Ant Group</a> 
</p>

<!-- <div align="center"><img src="images/VocalBench.png" width="25%"/></div> -->

**VocalBench** is a series of evaluation frameworks addressing speech interaction performance, covering diverse instruction formats and conversational scenarios. 

<!-- **Data and Code will be uploaded as soon as possible.** -->

## 👀 VocalBench Series

**[VocalBench (en)](https://arxiv.org/abs/2505.15727)** evaluates English conversational performance across semantics, acoustics, chat, and robustness, encompassing more than 10 major aspects, such as general knowledge, logical reasoning, and literary creation. 

**[VocalBench-DF](https://arxiv.org/abs/2510.15406)** is a framework for the systematic evaluation of disfluency across a multi-dimensional taxonomy, consisting of  linguistic realization disfluency and interaction interference disfluency.

**[VocalBench-zh](https://arxiv.org/abs/2511.08230)** is a systematic evaluation framework for Mandarin conversational abilities, addressing domestic knowledge, cultural and social characteristics, language style, and traditional customs, providing a reference for Chinese-capable speech interaction models.

## 📏 Evaluated models

- Speech LLMs: [LLaMA-Omni2](https://arxiv.org/abs/2505.02625), [Freeze-Omni](https://arxiv.org/abs/2411.00774), [Step-Audio-2-Mini](https://arxiv.org/abs/2507.16632), [GLM-4-Voice](https://arxiv.org/abs/2412.02612), [VITA-Audio](https://arxiv.org/abs/2505.03739), [Kimi-Audio](https://arxiv.org/abs/2504.18425), [VocalNet](https://arxiv.org/abs/2504.04060), VocalNet2, [MiMo-Audio](https://github.com/XiaomiMiMo/MiMo-Audio/blob/main/MiMo-Audio-Technical-Report.pdf)

- Omni LLMs: [Baichuan-Omni-1.5](https://arxiv.org/abs/2501.15368), [MiniCPM-o 2.6](https://openbmb.notion.site/MiniCPM-o-2-6-A-GPT-4o-Level-MLLM-for-Vision-Speech-and-Multimodal-Live-Streaming-on-Your-Phone-185ede1b7a558042b5d5e45e6b237da9), [Qwen2.5-Omni](https://arxiv.org/abs/2503.20215), [Qwen3-Omni](https://arxiv.org/abs/2509.17765)

## 🏆 Leaderboard

<div align="center">
  <table style="margin: 0 auto; text-align: center;">
    <thead>
      <tr>
         <th class="tg-c3ow" colspan="14"></th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: none;">
        <td rowspan="2">Model</td>
        <td>Knowledge</td>
        <td>Reasoning</td>
        <td>Creativity</td>
        <td>Fluency</td>
        <td>Clarity</td>
        <td>Single-round</td>
        <td>Multi-round</td>
        <td>Instruction Following</td>
        <td>Emotional Empathy</td>
        <td>Safety Alignment</td>
        <td>Code Switching</td>
        <td>Robustness</td>
        <td rowspan="2">Overall</td>
      </tr>
      <tr>
        <td>ACC(%)</td>
        <td>ACC(%)</td>
        <td>Score</td>
        <td>UTMOS</td>
        <td>PER(%)</td>
        <td>Score</td>
        <td>ACC(%)</td>
        <td>FR(%)</td>
        <td>EER(%)</td>
        <td>RR(%)</td>
        <td>PR(%)</td>
        <td>Avg PR (%)</td>
      </tr>
      <tr>
        <td>LLaMA-Omni2-7B-Bilingual</td>
        <td>36.4</td>
        <td>32.080</td>
        <td>2.704</td>
        <td><b>3.664<br></td>
        <td>1.941</td>
        <td>3.365</td>
        <td>64.50</td>
        <td>23.3</td>
        <td>43.6</td>
        <td>41.00</td>
        <td>48.83</td>
        <td>85.423</td>
        <td>56.253</td>
      </tr>
      <tr>
        <td>Freeze-Omni</td>
        <td>51.0</td>
        <td>40.188</td>
        <td>2.692</td>
        <td>3.551</td>
        <td>1.617</td>
        <td>3.460</td>
        <td> - </td>
        <td>14.6</td>
        <td>38.0</td>
        <td>70.75</td>
        <td>49.79</td>
        <td>69.109</td>
        <td>57.675</td>
      </tr>
      <tr>
        <td>Step-Audio-2-Mini</td>
        <td>57.1</td>
        <td>54.994</td>
        <td>3.308</td>
        <td>3.290</td>
        <td>33.947</td>
        <td>3.810</td>
        <td>58.00</td>
        <td>42.6</td>
        <td>35.0</td>
        <td>77.00</td>
        <td>58.11</td>
        <td>96.042</td>
        <td>58.602</td>
      </tr>
      <tr>
        <td>Baichuan-Omni-1.5</td>
        <td>55.5</td>
        <td>59.107</td>
        <td>3.275</td>
        <td>2.474</td>
        <td>21.334</td>
        <td>3.605</td>
        <td>-</td>
        <td>31.7</td>
        <td>44.9</td>
        <td>87.25</td>
        <td>55.92</td>
        <td><b>99.357<br></td>
        <td>58.983</td>
      </tr>
      <tr>
        <td>MiniCPM-o 2.6</td>
        <td>50.4</td>
        <td>53.937</td>
        <td>3.250</td>
        <td>3.079</td>
        <td>14.234</td>
        <td>3.585</td>
        <td>69.25</td>
        <td>33.8</td>
        <td>54.0</td>
        <td>78.25</td>
        <td>64.36</td>
        <td>82.213</td>
        <td>59.120</td>
      </tr>
      <tr>
        <td>VocalNet2-1.7B</td>
        <td>32.4</td>
        <td>45.123</td>
        <td>3.033</td>
        <td>2.841</td>
        <td>1.345</td>
        <td>3.355</td>
        <td>58.50</td>
        <td>24.3</td>
        <td>41.8</td>
        <td>66.50</td>
        <td>62.41</td>
        <td>85.650</td>
        <td>59.477</td>
      </tr>
      <tr>
        <td>VocalNet-ML</td>
        <td>42.5</td>
        <td>46.769</td>
        <td>2.825</td>
        <td>3.137</td>
        <td>1.930</td>
        <td>3.185</td>
        <td>62.25</td>
        <td>33.5</td>
        <td>31.4</td>
        <td>89.00</td>
        <td>34.05</td>
        <td>88.449</td>
        <td>62.741</td>
      </tr>
      <tr>
        <td>GLM-4-Voice</td>
        <td>52.6</td>
        <td>48.766</td>
        <td>3.246</td>
        <td>2.610</td>
        <td>2.190</td>
        <td>3.630</td>
        <td>69.25</td>
        <td>34.9</td>
        <td>58.0</td>
        <td>76.50</td>
        <td>45.75</td>
        <td>80.859</td>
        <td>64.567</td>
      </tr>
      <tr>
        <td>VITA-Audio-Plus-Vanilla</td>
        <td>40.8</td>
        <td>65.922</td>
        <td>3.179</td>
        <td>2.420</td>
        <td>5.090</td>
        <td>4.120</td>
        <td>-</td>
        <td>36.4</td>
        <td>43.0</td>
        <td>80.50</td>
        <td>74.86</td>
        <td>95.139</td>
        <td>65.951</td>
      </tr>
      <tr>
        <td>Qwen2.5-Omni</td>
        <td>56.8</td>
        <td>72.268</td>
        <td>3.025</td>
        <td>2.838</td>
        <td><b>0.712<br></td>
        <td>3.250</td>
        <td>73.75</td>
        <td>33.6</td>
        <td>48.6</td>
        <td>72.50</td>
        <td>54.67</td>
        <td>94.172</td>
        <td>67.891</td>
      </tr>
      <tr>
        <td>VocalNet2-8B</td>
        <td>55.8</td>
        <td>68.038</td>
        <td>3.404</td>
        <td>2.827</td>
        <td>1.245</td>
        <td>3.805</td>
        <td>75.50</td>
        <td>42.4</td>
        <td>42.4</td>
        <td>78.25</td>
        <td>66.05</td>
        <td>89.080</td>
        <td>69.296</td>
      </tr>
      <tr>
        <td>Kimi-Audio</td>
        <td>59.6</td>
        <td>66.863</td>
        <td>3.318</td>
        <td>2.494</td>
        <td>0.826</td>
        <td>3.165</td>
        <td>70.50</td>
        <td>50.2</td>
        <td>41.0</td>
        <td>81.25</td>
        <td>65.63</td>
        <td>94.347</td>
        <td>69.503</td>
      </tr>
      <tr>
        <td>MiMo-Audio-Instruct</td>
        <td>65.6</td>
        <td>70.035</td>
        <td>4.271</td>
        <td>2.149</td>
        <td>2.775</td>
        <td>4.730</td>
        <td>-</td>
        <td>52.3</td>
        <td>47.6</td>
        <td><b>94.50<br></td>
        <td>73.76</td>
        <td>93.487</td>
        <td>76.178</td>
      </tr>
      <tr>
        <td>Qwen3-Omni</td>
        <td><b>91.8<br></td>
        <td><b>83.784<br></td>
        <td><b>4.358<br></td>
        <td>2.766</td>
        <td>12.181</td>
        <td><b>4.985<br></td>
        <td><b>86.25<br></td>
        <td><b>73.3<br></td>
        <td>40.0</td>
        <td>92.25</td>
        <td><b>90.89<br></td>
        <td>98.795</td>
        <td><b>78.439<br></td>
      </tr>
      <tr>
        <td colspan="14">Cascade System</td>
      </tr>
      <tr>
        <td>Whisper + Qwen3-8B + CosyVoice2</td>
        <td>64.5</td>
        <td><b>73.090<br></td>
        <td>3.808</td>
        <td>2.409</td>
        <td><b>0.823<br></td>
        <td><b>4.810<br></td>
        <td><b>83.00<br></td>
        <td><b>60.8<br></td>
        <td>40.5</td>
        <td>89.50</td>
        <td>67.43</td>
        <td>80.802</td>
        <td>74.604</td>
      </tr>
    <thead>
      <tr>
         <th class="tg-c3ow" colspan="14"></th>
      </tr>
    </thead>
    </tbody>
  </table>
</div>

<br> 
<br> 

## 📐 Evaluation Metrics

- Accuracy (ACC): For knowledge, reasoning, and multi-round evaluation, we use accuracy as an objective indicator.
- Score: For literary creativity and single-round dialogue, we use LLM-as-a-Judge to score on a 1-5 range.
- Preserve Rate (PR): For code Switching and robustness evaluation, we define the preserve rate as the proportion of correct instances / scores within multilingual / noisy inputs compared to monolingual / clean conditions.
- Refusal Rate (RR) and Following Rate (FR): For safety alignment set, we report the refusal rate of each model. For instruction following set, we use following rate.
- Emotional Empathy Rate (EER): For emotional empathy evaluation, we define emotional empathy rate as the proportion that model response shows empathy on both semantic meanings and acoustic tones.
- UTMOS and phoneme error rate (PER) are used for acoustic quality.  

## 📌 Evaluation Methods

- AK and Path Modification

```python
# utils/config.py

keys = ["YOUR_QWEN_KEY_1",
        "YOUR_QWEN_KEY_2",
        "YOUR_QWEN_KEY_3"]
EMOTION2VEC_PLUS_LARGE = '/workspace/tools/emotion2vec_plus_large'
WHISPER_LARGE_V3 = '/workspace/tools/whisper'
```

```bash
cd /workspace/tools/emotion2vec_plus_large
echo -e "angry\nunuse_0\nunuse_1\nhappy\nneutral\nunuse_2\nsad\nsurprised\n<unk>" > tokens.txt
```

- Qwenmax-eval for Most Evaluation Sets

```bash
# e.g. knowledge
cd utils
python3 knowledge.py --input_json ../model_output/qwen3-omni/json_asr/chinese_knowledge.json --output_json ../model_output/qwen3-omni/result/chinese_knowledge.json
```

- Additional Acoustic Constraints for Instruction Following and Emotional Empathy Set 
```bash
# e.g. Instruction Following
python3 instruction_semantic.py --input_json ../model_output/qwen3-omni/json/instruction_following.json --output_json ../model_output/qwen3-omni/result/instruction_following.json
python3 instruction_full.py --eval_json ../model_output/qwen3-omni/result/instruction_following.json
# Emotional Empathy
python3 emotion_semantic.py --input_json ../model_output/qwen3-omni/json/emotion.json --output_json ../model_output/qwen3-omni/result/emotion_semantic.json
python3 emotion_acoustic.py --wav_dir ../model_output/qwen3-omni/wav/emotion --output_json ../model_output/qwen3-omni/result/emotion_acoustic.json
python3 emotional_empathy_rate.py --semantic_json ../model_output/qwen3-omni/result/emotion_semantic.json --acoustic_json ../model_output/qwen3-omni/result/emotion_acoustic.json
```

- For Speech Recognition 

```bash
python3 whisper_asr.py --input_json ../model_output/qwen3-omni/json/chinese_knowledge.json --output_json ../model_output/qwen3-omni/json_asr/chinese_knowledge.json --audio_dir ../model_output/qwen3-omni/wav/chinese_knowledge
```

## 🌞 Acknowledgements

- [Whisper](https://huggingface.co/openai/whisper-large-v3): VocalBench-zh uses Whisper-large-v3 for speech recognition.
- [pypinyin](https://github.com/mozillazg/python-pinyin): VocalBench-zh uses pypinyin for phoneme error rate calculation.
- [emotion2vec](https://huggingface.co/emotion2vec/emotion2vec_plus_large): VocalBench-zh uses emotion2vec_plus_large for emotion recognition.
- [UTMOS](https://github.com/sarulab-speech/UTMOS22): VocalBench uses UTMOS to quantify the acoustic quality.
- [Qwen2.5-Max](https://qwenlm.github.io/blog/qwen2.5-max/): VocalBench-zh uses Qwen2.5-Max for LLM evaluation.

<br> 
<br> 

## ⚖️ License

This repository is released under the Apache-2.0 license as found in the [LICENSE](LICENSE) file.

<br> 
<br> 

## 💡 Citation
If you find our benchmark helpful, please consider citing our papers 📝 and staring us ⭐️！

```bib
@article{liu2025vocalbench-zh,
  title={VocalBench-zh: Decomposing and Benchmarking the Speech Conversational Abilities in Mandarin Context},
  author={Liu, Heyang and Cheng, Ziayng and Wang, Yuhao and Liu, Hongcheng and Li, Yiqi and Wu, Ronghua and Gu, Qunshan and Wang, Yanfeng and Wang, Yu},
  journal={arXiv preprint arXiv:2511.08230},
  year={2025}
}
```
