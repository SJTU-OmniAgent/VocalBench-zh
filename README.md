<div align="center">


# **📈VocalBench-zh: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models**
<!-- # 🎧VocalNet: Speech LLM with Multi-Token Prediction for Faster and High-Quality Generation -->
<!-- <strong>English | 
[Chinese](./README_zh.md)</strong> -->

</div>

<p align="center">
HuggingFace <a href="https://huggingface.co/datasets/VocalNet/VocalBench-zh">🤗</a> | Paper <a href="https://arxiv.org/abs/2505.15727">📖</a> 
</p>
<p align="center">
Shanghai Jiao Tong University</a>  |  Ant Group</a> 
</p>

<!-- <div align="center"><img src="images/VocalBench.png" width="25%"/></div> -->

**VocalBench** is a series of evaluation frameworks addressing speech interaction performance, covering diverse instruction formats and conversational scenarios. 

<!-- **Data and Code will be uploaded as soon as possible.** -->

## 👀 VocalBench Series

**[VocalBench-en](https://github.com/SJTU-OmniAgent/VocalBench)** evaluates English conversational performance across semantics, acoustics, chat, and robustness, encompassing over 10 major aspects, such as general knowledge, logical reasoning, and literary creation. 

**[VocalBench-zh](https://github.com/SJTU-OmniAgent/VocalBench-zh)** is a systematic evaluation framework for Mandarin conversational abilities, addressing domestic knowledge, cultural and social characteristics, language style, and traditional customs, providing a reference for Chinese-capable speech interaction models.

**[VocalBench-DF](https://arxiv.org/abs/2510.15406)** is a framework for the systematic evaluation of disfluency across a multi-dimensional taxonomy, consisting of  linguistic realization disfluency and interaction interference disfluency.


## 📐 Evaluation Metrics

- Accuracy (ACC): For knowledge, reasoning, and multi-round evaluation, we use accuracy as an objective indicator.
- Score: For literary creativity and single-round dialogue, we use LLM-as-a-Judge to score on a 1-5 range.
- Preserve Rate (PR): For code Switching and robustness evaluation, we define the preserve rate as the proportion of correct instances / scores within multilingual / noisy inputs compared to monolingual / clean conditions.
- Refusal Rate (RR) and Following Rate (FR): For safety alignment set, we report the refusal rate of each model. For instruction following set, we use following rate.
- Emotional Empathy Rate (EER): For emotional empathy evaluation, we define emotional empathy rate as the proportion that model response shows empathy on both semantic meanings and acoustic tones.
- UTMOS and phoneme error rate (PER) are used for acoustic quality.  


## 🏆 Leaderboard

<div align="center">
  <table style="margin: 0 auto; text-align: center;">
    <thead>
      <tr>
         <th class="tg-c3ow" colspan="16"></th>
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
        <td>Dialect</td>
        <td>Latency</td>
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
        <td>PR(%)</td>
        <td>RTF</td>
        <td>PR(%)</td>
      </tr>
      <tr>
        <td colspan="16">Tiny-sized Models</td>
      </tr>
      <tr>
        <td>SLAM-Omni</td>
        <td>6.3</td>
        <td>7.19</td>
        <td>2.034</td>
        <td><b>3.035<br></td>
        <td>3.944</td>
        <td>2.450</td>
        <td>14.00</td>
        <td>6.9</td>
        <td>12.3</td>
        <td>59.25</td>
        <td>-</td>
        <td><b>44.48<br></td>
        <td>0.5637</td>
        <td>78.364</td>
        <td>41.852</td>
      </tr>
      <tr>
        <td>VocalNet2-1.7B</td>
        <td><b>32.4<br></td>
        <td><b>45.12<br></td>
        <td><b>3.033<br></td>
        <td>2.841</td>
        <td><b>1.345<br></td>
        <td><b>3.355<br></td>
        <td><b>58.50<br></td>
        <td><b>24.3<br></td>
        <td><b>41.8<br></td>
        <td><b>66.50<br></td>
        <td><b>62.41<br></td>
        <td>40.46</td>
        <td><b>0.3103<br></td>
        <td><b>85.650<br></td>
        <td><b>59.477<br></td>
      </tr>
      <tr>
        <td colspan="16">Base-sized Models</td>
      </tr>
      <tr>
        <td>LLaMA-Omni2-7B-Bilingual</td>
        <td>36.4</td>
        <td>32.08</td>
        <td>2.704</td>
        <td><b>3.664<br></td>
        <td>1.941</td>
        <td>3.365</td>
        <td>64.50</td>
        <td>23.3</td>
        <td>43.6</td>
        <td>41.00</td>
        <td>48.83</td>
        <td>27.96</td>
        <td>0.4555</td>
        <td>85.423</td>
        <td>56.253</td>
      </tr>
      <tr>
        <td>Freeze-Omni</td>
        <td>51.0</td>
        <td>40.19</td>
        <td>2.692</td>
        <td>3.551</td>
        <td>1.617</td>
        <td>3.460</td>
        <td> - </td>
        <td>14.7</td>
        <td>38.0</td>
        <td>70.75</td>
        <td>49.79</td>
        <td>33.04</td>
        <td>0.5561</td>
        <td>69.109</td>
        <td>57.685</td>
      </tr>
      <tr>
        <td>Step-Audio-2-Mini</td>
        <td>57.1</td>
        <td>54.99</td>
        <td>3.308</td>
        <td>3.290</td>
        <td>33.947</td>
        <td>3.810</td>
        <td>58.00</td>
        <td>42.7</td>
        <td>35.0</td>
        <td>77.00</td>
        <td>58.11</td>
        <td>68.48</td>
        <td>3.3519</td>
        <td>96.042</td>
        <td>58.612</td>
      </tr>
      <tr>
        <td>MiniCPM-o 2.6</td>
        <td>50.4</td>
        <td>53.94</td>
        <td>3.250</td>
        <td>3.079</td>
        <td>14.234</td>
        <td>3.585</td>
        <td>69.25</td>
        <td>34.3</td>
        <td>54.0</td>
        <td>78.25</td>
        <td>64.36</td>
        <td>36.04</td>
        <td>0.4682</td>
        <td>82.213</td>
        <td>59.170</td>
      </tr>
      <tr>
        <td>Baichuan-Omni-1.5</td>
        <td>55.5</td>
        <td>59.11</td>
        <td>3.275</td>
        <td>2.474</td>
        <td>21.334</td>
        <td>3.605</td>
        <td>-</td>
        <td>33.7</td>
        <td>44.9</td>
        <td>87.25</td>
        <td>55.92</td>
        <td>60.05</td>
        <td>1.4554</td>
        <td><b>99.357<br></td>
        <td>59.183</td>
      </tr>
      <tr>
        <td>VocalNet-ML</td>
        <td>42.5</td>
        <td>46.77</td>
        <td>2.825</td>
        <td>3.137</td>
        <td>1.930</td>
        <td>3.185</td>
        <td>62.25</td>
        <td>33.5</td>
        <td>31.4</td>
        <td>89.00</td>
        <td>34.05</td>
        <td>40.24</td>
        <td><b>0.2773<br></td>
        <td>88.449</td>
        <td>62.741</td>
      </tr>
      <tr>
        <td>GLM-4-Voice</td>
        <td>52.6</td>
        <td>48.77</td>
        <td>3.246</td>
        <td>2.610</td>
        <td>2.190</td>
        <td>3.630</td>
        <td>69.25</td>
        <td>35.4</td>
        <td><b>58.0<br></td>
        <td>76.50</td>
        <td>45.75</td>
        <td>27.88</td>
        <td>0.6568</td>
        <td>80.859</td>
        <td>64.617</td>
      </tr>
      <tr>
        <td>VITA-Audio</td>
        <td>40.8</td>
        <td>65.92</td>
        <td>3.179</td>
        <td>2.420</td>
        <td>5.090</td>
        <td>4.120</td>
        <td>-</td>
        <td>36.6</td>
        <td>43.0</td>
        <td>80.50</td>
        <td><b>74.86<br></td>
        <td>69.65</td>
        <td>0.4899</td>
        <td>95.139</td>
        <td>65.971</td>
      </tr>
      <tr>
        <td>Qwen2.5-Omni</td>
        <td>56.8</td>
        <td><b>72.27<br></td>
        <td>3.025</td>
        <td>2.838</td>
        <td><b>0.712<br></td>
        <td>3.250</td>
        <td>73.75</td>
        <td>33.8</td>
        <td>48.6</td>
        <td>72.50</td>
        <td>54.67</td>
        <td><b>72.01<br></td>
        <td>1.7970</td>
        <td>94.172</td>
        <td>67.911</td>
      </tr>
      <tr>
        <td>VocalNet2-8B</td>
        <td>55.8</td>
        <td>68.04</td>
        <td>3.404</td>
        <td>2.827</td>
        <td>1.245</td>
        <td>3.805</td>
        <td><b>75.50<br></td>
        <td>42.6</td>
        <td>42.4</td>
        <td>78.25</td>
        <td>66.05</td>
        <td>41.22</td>
        <td>0.3593</td>
        <td>89.080</td>
        <td>69.316</td>
      </tr>
      <tr>
        <td>Kimi-Audio</td>
        <td>59.6</td>
        <td>66.86</td>
        <td>3.318</td>
        <td>2.494</td>
        <td>0.826</td>
        <td>3.165</td>
        <td>70.50</td>
        <td>51.2</td>
        <td>41.0</td>
        <td>81.25</td>
        <td>65.63</td>
        <td>48.05</td>
        <td>0.7205</td>
        <td>94.347</td>
        <td>69.603</td>
      </tr>
      <tr>
        <td>MiMo-Audio-Instruct</td>
        <td><b>65.6<br></td>
        <td>70.04</td>
        <td><b>4.271<br></td>
        <td>2.149</td>
        <td>2.775</td>
        <td><b>4.730<br></td>
        <td>-</td>
        <td><b>52.4<br></td>
        <td>47.6</td>
        <td><b>94.50<br></td>
        <td>73.76</td>
        <td>46.60</td>
        <td>0.6856</td>
        <td>93.487</td>
        <td>76.188</td>
      </tr>
      <tr>
        <td colspan="16">Large-sized Models</td>
      </tr>
      <tr>
        <td>Qwen3-Omni</td>
        <td><b>91.8<br></td>
        <td><b>83.78<br></td>
        <td><b>4.358<br></td>
        <td>2.766</td>
        <td>12.181</td>
        <td><b>4.985<br></td>
        <td><b>86.25<br></td>
        <td><b>73.3<br></td>
        <td>40.0</td>
        <td>92.25</td>
        <td><b>90.89<br></td>
        <td>70.60</td>
        <td>-</td>
        <td>98.795</td>
        <td><b>78.439<br></td>
      </tr>
      <tr>
        <td colspan="16">Cascade System & Real Time API</td>
      </tr>
      <tr>
        <td>Qwen-Omni-Turbo</td>
        <td>55.7</td>
        <td>68.24</td>
        <td>3.094</td>
        <td>3.108</td>
        <td>1.190</td>
        <td>3.188</td>
        <td>71.00</td>
        <td>34.2</td>
        <td>38.5</td>
        <td>68.25</td>
        <td>33.33</td>
        <td><b>74.51<br></td>
        <td>-</td>
        <td>94.375</td>
        <td>66.318</td>
      </tr>
      <tr>
        <td>Cascade (Qwen3-8B)</td>
        <td>64.5</td>
        <td>73.09</td>
        <td>3.808</td>
        <td>2.409</td>
        <td>0.823</td>
        <td>4.810</td>
        <td>83.00</td>
        <td>60.9</td>
        <td>40.5</td>
        <td>89.50</td>
        <td>67.43</td>
        <td>35.64</td>
        <td>-</td>
        <td>80.802</td>
        <td>74.614</td>
      </tr>
      <tr>
        <td>Cascade (Qwen3-Max)</td>
        <td><b>92.2<br></td>
        <td><b>85.08<br></td>
        <td>4.246</td>
        <td>2.535</td>
        <td>6.635</td>
        <td>4.845</td>
        <td><b>89.25<br></td>
        <td><b>76.8<br></td>
        <td>42.8</td>
        <td><b>98.25<br></td>
        <td>86.03</td>
        <td>42.40</td>
        <td>-</td>
        <td>83.299</td>
        <td><b>79.724<br></td>
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
@article{liu2025vocalbench,
  title={VocalBench: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models},
  author={Liu, Heyang and Wang, Yuhao and Cheng, Ziyang and Wu, Ronghua and Gu, Qunshan and Wang, Yanfeng and Wang, Yu},
  journal={arXiv preprint arXiv:2505.15727},
  year={2025}
}
```
