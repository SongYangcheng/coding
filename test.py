import jieba
import re

def wordcount(text):
    # 去除标点符号和回车符，只保留单词
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace('\n', ' ')
    
    # 使用jieba分词
    words_list = jieba.lcut(text)
    
    # 将每个单词的第一个字母变为小写
    words_list = [word[0].lower() + word[1:] if word else word for word in words_list]
    
    word_count_dict = {}
    for word in words_list:
        if word.strip():  # 过滤掉空字符串
            if word in word_count_dict:
                word_count_dict[word] += 1
            else:
                word_count_dict[word] = 1
    
    return word_count_dict

text = """
Got this panda plush toy for my daughter's birthday,
who loves it and takes it everywhere. It's soft and
super cute, and its face has a friendly look. It's
a bit small for what I paid though. I think there
might be other options that are bigger for the
same price. It arrived a day earlier than expected,
so I got to play with it myself before I gave it
to her.
"""

result = wordcount(text)
print(result)