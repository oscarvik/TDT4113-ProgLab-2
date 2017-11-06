import math
import re


pos_w = {"nice":0.98, "superb":0.89, "amazed":0.504, "bad":0.24, "terrible":0.06, "suck":0.33}
neg_w = {"bad":0.76, "terrible":0.94, "amazed":0.496, "suck":0.67,"nice":0.02,"superb":0.11}


positive_reviews = []
negative_reviews = []
file_lst = [["this","was","a","nice","movie","amazed"],["hated","movie","amazed","terrible"],["not","bad","superb","movie","nice"]]
for file in file_lst:
    pos = 0
    neg = 0
    for word in file:
        if word in pos_w.keys():
            pos += math.log(pos_w.get(word))
        else:
            pos += math.log(0.01)
        if word in neg_w.keys():
            neg += math.log(neg_w.get(word))
        else:
            neg += math.log(0.01)

    if pos > neg:
        positive_reviews.append(file)
    else:
        negative_reviews.append(file)
    print("pos: "+str(pos)+"\tneg: "+str(neg))

print("pos: " + str(positive_reviews))
print("neg: "+str(negative_reviews))



stopwords = re.findall(r"[\w][\w]*'?\w?", open("/Users/OscarVik/Documents/ProgLab2/Oving4/data/stop_words.txt").read().lower())
print("\n"+str(stopwords))
print('an' in stopwords)
test_list = ['', 'need', 'south', 'now', 'an', 'from', 'i', 'for', 'settingthis', 'images', 'dummy', 'more', 'feel', 'took', 'almost', 'what', 'anyone', 'not', 'to', 'much','an', 'comments', 'while', 'issue', 'bassinger', 'other', 'lovely', 'a', 'an', 'i']
stripped = []
for element in test_list:
    if element not in stopwords and element !='':
        stripped.append(element)
#print(stripped)


    def read(self,filename):
        file = open(filename)
        text = file.read()
        file.close()
        file_list = text.split(" ")
        lower_list = []
        for word in file_list:
            stripped_word = ''.join(c for c in word if c not in "'<>\"!#$%&=?:;`´.*,\/-_\n()").lower()
            if stripped_word.endswith("br"):
                stripped_word = stripped_word[:-2]
            lower_list.append(stripped_word)
        if self.n_gram == 2:
            for i in range(len(lower_list)-1):
                lower_list.append(lower_list[i]+"-"+lower_list[i+1])
        elif self.n_gram == 3:
            for i in range(len(lower_list)-2):
                lower_list.append(lower_list[i]+"-"+lower_list[i+1]+"-"+lower_list[i+2])
        unique = list(set(lower_list))
        return unique
