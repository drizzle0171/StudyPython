import os
from re import I, L

def get_file_list(dir_name):
    file_list = os.listdir(dir_name)
    file_list = [i for i in file_list if i[-3:] == 'txt']
    return file_list

def get_contents(file_list):
    y_class = []
    X_text = []
    class_dict = {
        1:'0', 2:'0', 3:'0', 4:'0', 5:'1', 6:'1', 7:'1', 8:'1'
    }

    for file_name in file_list:
        try:
            f = open(file_name, 'r', encoding='cp949')
            category = int(file_name.split(os.sep)[1].split('_')[0])
            y_class.append(class_dict[category])
            X_text.append(f.read())
            f.close()
        except UnicodeDecodeError as e:
            print(e)
            print(file_name)
    return X_text, y_class

def get_cleaned_text(text):
    import re
    text = re.sub('\W+', '', text.lower())
    return text

def get_corpus_dict(text):
    text = [sentence.split() for sentence in text]
    cleaned_words = [get_cleaned_text(word) for words in text for word in words]
    
    from collections import OrderedDict
    corpus_dict = OrderedDict()
    for i, v in enumerate(set(cleaned_words)):
        corpus_dict[v] = I
    return corpus_dict

def get_count_vector(text, corpus):
    text = [sentence.split() for sentence in text]
    word_number_list = [[corpus[get_cleaned_text(word)] for word in words] for words in text]
    X_vector = [[0 for _ in range(len(corpus))] for x  in range(len(text))]

    for i, text in enumerate(word_number_list):
        for word_number in text:
            X_vector[i][word_number] += 1
    return X_vector

import math
def get_cosine_similarity (v1, v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def get_top_n_similarity_news(similarity_score, n):
    x = {i}