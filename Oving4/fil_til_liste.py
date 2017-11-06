import glob
import re
from math import *

def read1(filename, stopwords):
    file = open(filename)
    text = file.read()
    print(text)
    file.close()
    file_list = text.split(" ")
    lower_list = []
    for word in file_list:
        stripped_word = ''.join(c for c in word if c not in "'<>\"!#$%&=?:;`´.*,\/-_\n()").lower()
        if stripped_word.endswith("br"):
            stripped_word = stripped_word[:-2]
        lower_list.append(stripped_word)
    unique = list(set(lower_list))
    stripped_unique = []
    for word in unique:
        if word != '' and word not in stopwords:
            stripped_unique.append(word)
    return stripped_unique

def read2(filename, stopwords):
    file_list = re.findall(r"[\w][\w]*'?\w'?", open(filename).read().lower())
    unique = list(set(file_list))
    stripped_unique = []
    for word in unique:
        stripped_word = re.sub('[^a-åA-Å0-9]',"",word)
        if stripped_word.endswith("br"):
            stripped_word = stripped_word[:-2]
        if stripped_word != '' and stripped_word not in stopwords:
            stripped_unique.append(stripped_word)
    return stripped_unique

def read3(filename, stopwords):
    file_list = re.findall(r"[\w][\w]*'?[\w][\w]?", open(filename).read().lower())
    unique = list(set(file_list))
    stripped_unique = []
    for word in unique:
        stripped_word = re.sub('[^a-åA-Å0-9]',"",word)
        if stripped_word.endswith("br"):
            stripped_word = stripped_word[:-2]
        if stripped_word != '' and stripped_word not in stopwords:
            stripped_unique.append(stripped_word)
    return stripped_unique



def main():
    stopwords = re.findall(r"[\w][\w]*'?\w?", open("/Users/OscarVik/Documents/ProgLab2/Oving4/data/stop_words.txt").read().lower())
    pos_files = glob.glob("/Users/OscarVik/Documents/ProgLab2/Oving4/data/alle/test/pos/*.txt")
    file2 = read2(pos_files[9],stopwords)
    #print(file2)
    file3 = read3(pos_files[9],stopwords)
    #print(file3)
    for i in range(200):
        print("i've" in re.findall(r"[\w][\w]*'?[\w][\w]?", open(pos_files[i]).read().lower()))
        print("i've" in re.findall(r"[\w][\w]*'?\w'?", open(pos_files[i]).read().lower()))
main()


