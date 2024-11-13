# -*- coding: utf-8 -*-

import re

def is_fixed_phrase(words, index):
    """判断是否是常见的固定短语"""
    if index < len(words) - 1:
        # 检查类似于 "a + 名词" 或 "the + 名词" 的结构
        if words[index].lower() in {"a", "an", "the"} and re.match(r'^[a-zA-Z]+$', words[index + 1]):
            return True
        # 检查由连词连接的短语
        if words[index + 1].lower() in {"of", "in", "on"}:
            return True
    return False

def split_text_with_flexible_limit_auto_phrases(text, max_chars_per_line=15, tolerance=3, max_words_per_line=4):
    words = text.split()  # 先按空格分割单词
    lines = []  # 存储最终的行内容
    current_line = []  # 临时存储当前行的单词
    current_length = 0  # 当前行的字符总数
    single_words_to_avoid = {"a", "an", "the"}  # 避免单独放在行尾的词

    i = 0
    while i < len(words):
        word = words[i]

        # 检查是否遇到常见的固定短语结构
        if is_fixed_phrase(words, i):
            word = f"{words[i]} {words[i + 1]}"
            i += 1  # 跳过下一个词，以免拆分固定短语

        # 计算加入新单词后的长度
        potential_length = current_length + len(word) + len(current_line)
        
        # 如果新单词加入后长度在允许范围内，且不超过最大单词数量，加入单词
        if potential_length <= max_chars_per_line + tolerance and len(current_line) < max_words_per_line:
            current_line.append(word)
            current_length += len(word)
        else:
            # 如果当前行最后一个单词是冠词之一，调整到下一行
            if current_line and current_line[-1].lower() in single_words_to_avoid:
                last_word = current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [last_word, word]
            else:
                # 当前行满足长度，换行
                lines.append(" ".join(current_line))
                current_line = [word]
            
            # 重置当前行的字符数
            current_length = sum(len(w) for w in current_line)

        i += 1
    
    # 把最后一行加入到结果中
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)

# 示例文本
text_with_spaces = (
    "Elizabeth as they drove along watched for the first appearance of Pemberley Woods "
    "with some perturbation and when at length they turned in at the lodge her spirits were "
    "in a high flutter The park was very large and contained great variety of ground They "
    "entered it in one of its lowest points and drove for some time through a beautiful wood "
    "stretching over a wide extent Elizabeth’s mind was too full for conversation but she saw "
    "and admired every remarkable spot and point of view They gradually ascended for half a mile "
    "and then found themselves at the top of a considerable eminence where the wood ceased and the "
    "eye was instantly caught by Pemberley House situated on the opposite side of a valley into "
    "which the road with some abruptness wound It was a large handsome stone building standing well "
    "on rising ground and backed by a ridge of high woody hills and in front a stream of some natural "
    "importance was swelled into greater but without any artificial appearance Its banks were neither "
    "formal nor falsely adorned Elizabeth was delighted She had never seen a place for which nature "
    "had done more or where natural beauty had been so little counteracted by an awkward taste"
)

# 获取格式化后的文本
formatted_text = split_text_with_flexible_limit_auto_phrases(text_with_spaces, max_chars_per_line=15, tolerance=3, max_words_per_line=4)

# 打印格式化后的文本
print("格式化后的文本：")
print(formatted_text)

# 将格式化结果保存到 txt 文件
with open("formatted_text_output.txt", "w", encoding="utf-8") as file:
    file.write("格式化后的文本：\n")
    file.write(formatted_text)
