import re

def calculate_per(Tra, Hyp):
    """
    计算中文音素序列的音素错误率 (Phoneme Error Rate, PER)。

    Args:
        Tra (list of list): 参考音素序列 (Transcription), 例如 [['sa1'], ['mu3'], ...]
        Hyp (list of list): 识别/假设音素序列 (Hypothesis), 例如 [['sa1'], ['mo2'], ...]

    Returns:
        tuple: (distance, length, per)
            - distance (int): 编辑距离 (Levenshtein Distance)
            - length (int): 参考序列 (Tra) 的长度
            - per (float): 音素错误率 = distance / length (如果 length > 0, 否则为 0.0)
    """
    len_Tra = len(Tra)
    len_Hyp = len(Hyp)
    dp = [[0] * (len_Hyp + 1) for _ in range(len_Tra + 1)]
    for i in range(len_Tra + 1):
        dp[i][0] = i
    for j in range(len_Hyp + 1):
        dp[0][j] = j

    for i in range(1, len_Tra + 1):
        for j in range(1, len_Hyp + 1):
            if Tra[i-1] == Hyp[j-1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )

    distance = dp[len_Tra][len_Hyp]
    length = len_Tra
    per = distance / length if length > 0 else 0.0

    return distance, length, per

def text_normalization(text):
    """
    将输入文本进行归一化处理：
    1. 将数字（整数和小数）转换为中文读法。
    2. 移除所有非中文字符（只保留汉字）。

    Args:
        text (str): 输入的原始文本。

    Returns:
        str: 归一化后的纯中文文本。
    """

    # 中文数字映射
    num_to_chinese = {
        '0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
        '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'
    }

    # 单位映射（用于整数部分）
    units = ['', '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千']

    def number_to_chinese(num_str):
        """将数字字符串（整数或小数）转换为中文读法"""
        if '.' in num_str:
            # 处理小数
            integer_part, decimal_part = num_str.split('.')
            integer_chinese = integer_to_chinese(integer_part)
            # 小数部分逐位读
            decimal_chinese = ''.join(num_to_chinese[digit] for digit in decimal_part)
            # 组合：整数部分 + "点" + 小数部分
            return integer_chinese + '点' + decimal_chinese
        else:
            # 处理整数
            return integer_to_chinese(num_str)

    def integer_to_chinese(integer_str):
        """将整数字符串转换为中文读法"""
        if integer_str == '0':
            return '零'

        length = len(integer_str)
        result = ''

        for i, digit in enumerate(integer_str):
            # 当前位的数值
            num = int(digit)
            # 当前位的单位（从个位开始）
            unit_index = length - i - 1
            unit = units[unit_index] if unit_index < len(units) else ''

            # 处理特殊情况
            if num == 0:
                # 如果当前是零，且不是末尾位
                if i < length - 1:
                    # 检查是否需要添加'零'，避免连续多个零
                    # 如果下一位不是零，或者当前位是万/亿的末尾位，则需要'零'
                    if (i + 1 < length and integer_str[i + 1] != '0') or unit in ['万', '亿']:
                        # 避免在“万”、“亿”后面连续出现“零”
                        if not (result and result[-1] == '零'):
                            result += '零'
                # 末尾的零不读
            else:
                # 非零数字
                result += num_to_chinese[digit]
                # 添加单位，但“十百千”在“万”或“亿”前，以及“一十”情况需要特殊处理
                if unit:
                    # 处理“一十” -> “十”的情况
                    if num == 1 and unit == '十' and i == 0 and length > 1:
                        # 只有在最高位是1且单位是十（即十几）时，省略“一”
                        # 例如：15 -> 十五，而不是一十五
                        pass # 单位已隐含，不添加“一”
                    else:
                        result += unit

        return result

    # 步骤1: 找出文本中的所有数字（整数或小数）
    # 使用正则表达式匹配数字模式：可选的负号，整数部分，可选的小数部分（点+数字）
    # 注意：这个正则表达式相对简单，能处理基本的正负整数和小数
    pattern = r'-?\d+(?:\.\d+)?'

    def replace_match(match):
        """替换函数，将匹配到的数字字符串转换为中文"""
        num_str = match.group(0)
        # 如果是负数，先处理负号
        if num_str.startswith('-'):
            return '负' + number_to_chinese(num_str[1:])
        else:
            return number_to_chinese(num_str)

    # 将文本中的所有数字替换为中文读法
    text_with_chinese_numbers = re.sub(pattern, replace_match, text)

    # 步骤2: 移除所有非中文字符（只保留汉字）
    # 使用正则表达式匹配并删除所有非汉字字符
    # 汉字的Unicode范围大致是 [\u4e00-\u9fff]
    normalized_text = re.sub(r'[^\u4e00-\u9fff]', '', text_with_chinese_numbers)

    return normalized_text
