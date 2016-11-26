import sys
import random
import string
import nltk
import re


'''
You need to install nltk.corpus.words, do it by
>>> import nltk
>>> nltk.download()
'''


class DetectHoneyWord(object):


    def __init__(self):
        self.wholeRockYou = set()
        self.frequency = []
        self.english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        i = 0
        with open("rockyou-withcount.txt", encoding = "ISO-8859-1") as f:
            for line in f:
                if i == 110:
                    break
                i += 1
                temp = line.strip(" ").strip("\n").split(" ")
                self.wholeRockYou.add(temp[1])
                self.frequency.append(temp[0])

    def isAscending(self, num):
        for i in range(1, len(num)):
            if int(num[i]) != (int(num[i-1]) + 1)%10:
                return False
        return True


    def isDescending(self, num):
        for i in range(1, len(num)):
            if (int(num[i]) + 1)%10 != int(num[i-1]):
                return False
        return True


    def isSame(self, num):
        for i in range(1, len(num)):
            if num[i] != num[i-1]:
                return False
        return True

    # in this function we first generate a dict of features for each honeyword, including:
    # id: the number in the honeywordsList (1-based)
    # word_blocks: all char array in honeyword
    # num_blocks: all num array
    # in_rockyou: whether the word is in rockyou
    # word_list: all valid dictionary word
    # num_pattern: all num array with some pattern (like ascending, descending, same digits)
    def getPassword(self, honeywordsList):
        hwlen = len(honeywordsList)
        wordFeatures = []
        for i, honeyword in enumerate(honeywordsList):
            wordFeatures.append({'id': i + 1})
            wordFeatures[-1]['word_blocks'] = re.findall(r'[\w\W]+', honeyword)
            wordFeatures[-1]['num_blocks'] = re.findall(r'[\d]+', honeyword)
            wordFeatures[-1]['in_rockyou'] = (honeyword in self.wholeRockYou)
            wordFeatures[-1]['word_list'] = []
            for word in wordFeatures[-1]['word_blocks']:
                if (len(word) > 1) and (word in self.english_vocab):
                    wordFeatures[-1]['word_list'].append(word)
            wordFeatures[-1]['num_pattern'] = []
            for num in wordFeatures[-1]['num_blocks']:
                if self.isAscending(num) or self.isDescending(num) or self.isSame(num):
                    wordFeatures[-1]['num_pattern'].append(num)

        dict_word, num_pattern_word = [], []
        in_rockyou, notin_rockyou = [], []
        rating = []
        maxRate = 0
        for feature in wordFeatures:
            rate = 0
            if feature['in_rockyou']:
                in_rockyou.append(feature['id'])
                rate += 1
            else:
                notin_rockyou.append(feature['id'])
            if feature['word_list']:
                dict_word.append(feature['id'])
                rate += 1
            if feature['num_pattern']:
                num_pattern_word.append(feature['id'])
                rate += 1
            rating.append(rate)
            maxRate = max(maxRate, rate)

        # if there is only one word (in / not in) rockyou, return it
        if len(in_rockyou) == 1:
            return in_rockyou[0]
        if len(notin_rockyou) == 1:
            return notin_rockyou[0]
        # if there is only one word containing valid dictionary word, return it
        if len(dict_word) == 1:
            return dict_word[0]
        # if there is only one word containing num pattern, return it
        if len(num_pattern_word) == 1:
            return num_pattern_word[0]

        # if we cannot single out one honeyword, randomly pick one from the highest rated ones
        maxRating = []
        for i in range(hwlen):
            if rating[i] == maxRate:
                maxRating.append(i + 1)

        return random.choice(maxRating)


def main(argv):
    if len(argv) != 4:
        print('''
        Usage:
        your_program.py m n filename
        ''')
        return
    # parse parameter
    m = int(argv[1])
    n = int(argv[2])
    infile = open(argv[3], 'r')

    hwDetector = DetectHoneyWord()
    # print(m, n, argv[3])
    i = 0
    for honeywords in infile.read().splitlines():
        honeywordsList = honeywords.split(',')
        assert(len(honeywordsList) == n)
        print(hwDetector.getPassword(honeywordsList), end="")
        i += 1
        if (i != m): print(',', end="")

if __name__ == "__main__":
    main(sys.argv)
