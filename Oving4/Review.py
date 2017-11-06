import re
import glob
import operator
from math import log
from time import time


class Review:

    def __init__(self,stopwords, n_gram, prune):
        self.stopwords = stopwords
        self.n_gram = n_gram
        self.prune = prune

    def read(self,filename):
        file_list = re.findall(r"[\w][\w]*'?[\w][\w]?", open(filename).read().lower())
        if self.n_gram > 0:
            file_list += ['-'.join(file_list[x:x+self.n_gram])for x in range(0,len(file_list)-self.n_gram+1)]
        unique = list(set(file_list))
        return unique

    def find_reoccurring_words(self, file_list):
        word_count = {}
        for filename in file_list:
            word_list = self.read(filename)
            for word in word_list:
                if word not in self.stopwords:
                    if word_count.keys().__contains__(word):
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
        return word_count

    def find_word_significance(self,main_dict,other_dict,nr_of_files):
        result_dict = {}
        for key in main_dict:
            if (main_dict.get(key)/nr_of_files) > self.prune:
                result_dict[key] = main_dict.get(key)/(main_dict.get(key)+other_dict.get(key, 0))
        return result_dict

    def classify_review(self, file_lst, pos_words, neg_words):
        positive_reviews, negative_reviews = 0, 0
        for filename in file_lst:
            pos, neg = 0, 0
            word_list = self.read(filename)
            for word in word_list:
                if word not in self.stopwords and (word in pos_words or word in neg_words):
                    if word in pos_words.keys():
                        pos += log(pos_words.get(word))
                    else:
                        pos += log(0.02)
                    if word in neg_words.keys():
                        neg += log(neg_words.get(word))
                    else:
                        neg += log(0.02)
            if pos > neg:
                positive_reviews += 1
            elif neg > pos:
                negative_reviews += 1
        return positive_reviews, negative_reviews

def main():
    start = time()
    #OPPRETTER LISTER FRA MEDFØLGENDE FILER
    pos_files = glob.glob("/Users/OscarVik/Documents/ProgLab2/Oving4/data/alle/test/pos/*.txt")
    neg_files = glob.glob("/Users/OscarVik/Documents/ProgLab2/Oving4/data/alle/test/neg/*.txt")
    stopwords = re.findall(r"[\w][\w]*'?[\w][\w]?", open("/Users/OscarVik/Documents/ProgLab2/Oving4/data/stop_words.txt").read().lower())
    trainfiles_pos = glob.glob("/Users/OscarVik/Documents/ProgLab2/Oving4/data/alle/train/pos/*.txt")
    trainfiles_neg = glob.glob("/Users/OscarVik/Documents/ProgLab2/Oving4/data/alle/train/neg/*.txt")
    nr_of_trainfiles = len(trainfiles_pos)+len(trainfiles_neg)

    #TRENING AV SYSTEM - {WORD: FREQUENCY}
    n_gram = 0
    prune = 0.015
    review = Review(stopwords, n_gram, prune)
    positive_words = review.find_reoccurring_words(trainfiles_pos)#dict med (key = ord) og (value = antall ganger brukt)
    negative_words = review.find_reoccurring_words(trainfiles_neg)

    #TRENING AV SYSTEM - SIGNIFIKANS
    pos_word_sign = review.find_word_significance(positive_words, negative_words, nr_of_trainfiles)#dict med (key = ord) og (value = signifikans)
    print("Mest signifikante ord i positive filmanmeldelser:\n"+str(sorted(pos_word_sign.items(), key=operator.itemgetter(1), reverse=True)))
    neg_word_sign = review.find_word_significance(negative_words, positive_words, nr_of_trainfiles)
    print("Mest signifikante ord i negative filmanmeldelser:\n"+str(sorted(neg_word_sign.items(), key=operator.itemgetter(1), reverse=True)))

    #TEST AV SYSTEM
    pos1, neg1 = review.classify_review(pos_files,pos_word_sign,neg_word_sign)#antall reviews programmet tror er positive(pos1) og negative(neg1) fra pos_files
    print("\nReultat '/alle/test/pos/*.txt': "+str(pos1/len(pos_files))+" %")
    pos2, neg2 = review.classify_review(neg_files,pos_word_sign,neg_word_sign)
    print("Reultat '/alle/test/neg/*.txt': "+str(neg2/len(neg_files))+" %")

    print("TOT-resultat: "+str((neg2+pos1)/(len(pos_files)+len(neg_files)))+" %")
    end = time()
    print("\nTID: "+str('{0:.3g}'.format(end-start))+" s")
main()

