import sys
import random
import string

class HoneyWord(object):


    def __init__(self):
        self.wholeRockYou = []
        self.frequency = []
        i = 0
        with open("rockyou-withcount.txt", encoding = "ISO-8859-1") as f:
            for line in f:
                if i == 110:
                    break
                i += 1
                temp = line.strip(" ").strip("\n").split(" ")
                self.wholeRockYou.append(temp[1])
                self.frequency.append(temp[0])


    def WithOutTrainingSet(self, n, password):
        passwordLen = len(password)
        # n = n - 1 # adjustment term

        honeywords = []

        word_blocks_haha = []
        curr_word = ""

        for i, c in enumerate(password): # loop used to find word blocks, or groups of letters or numbers, that can be permuted
            if c.isalpha():
                curr_word = curr_word + c
                if i != passwordLen - 1:
                    if not password[i+1].isalpha():
                        word_blocks_haha.append(curr_word)
                        curr_word = ""
                else:
                    word_blocks_haha.append(curr_word)
            elif c.isdigit():
                curr_word = curr_word + c
                if i != passwordLen - 1:
                    if not password[i+1].isdigit():
                        word_blocks_haha.append(curr_word)
                        curr_word = ""
                else:
                    word_blocks_haha.append(curr_word)
            else:
                curr_word = curr_word + c
                if i != passwordLen - 1:
                    if (password[i+1].isdigit() or password[i+1].isalpha()):
                        word_blocks_haha.append(curr_word)
                        curr_word = ""
                else:
                    word_blocks_haha.append(curr_word)
        numOfBlocks = len(word_blocks_haha)

        # handles word based transformations
        while(len(honeywords) < n):
            honeyword = ""
            honeyword = password # let further attempts take over
			#print(word_blocks_haha)
            word_blocks = word_blocks_haha[:]
            if numOfBlocks > 1:
                for i in range(numOfBlocks):
                    roll1 = random.randint(1, 100)
                    if roll1 <= 10:
                        continue
                    if 11 <= roll1 <= 45:
                    # add one or two characters
                        roll2 = random.randint(1,100)
                        index = random.randint(0,numOfBlocks-1)
                        if roll2 > 95:
                            word_blocks[index] += random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?")
                            word_blocks[index] += random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?")
                        else:
                            word_blocks[index] += random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?")

                    if 46 <= roll1 <= 60:
                    # delete one or two characters
                        roll2 = random.randint(1,100)
                        index = random.randint(0,numOfBlocks-1)
                        if roll2 > 95:
                            for i in [0,1]:
                                if len(word_blocks[index]) > 1:
                                    word_blocks[index].replace(word_blocks[index][random.randint(0, len(word_blocks[index])-1)], "")
                        else:
                            if len(word_blocks[index]) > 1:
                                word_blocks[index].replace(word_blocks[index][random.randint(0, len(word_blocks[index])-1)], "")

                    if 61 <= roll1 <= 100:
                    # change one or two characters
                        roll2 = random.randint(1,100)
                        index = random.randint(0,numOfBlocks-1)
                        if roll2 > 85:
                            word_blocks[index].replace(word_blocks[index][random.randint(0, len(word_blocks[index])-1)], random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?"))
                            word_blocks[index].replace(word_blocks[index][random.randint(0, len(word_blocks[index])-1)], random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?"))
                        else:
                            word_blocks[index].replace(word_blocks[index][random.randint(0, len(word_blocks[index])-1)], random.choice(string.ascii_letters+string.digits+"~!@#$%^&*=/?"))



            # block permutation (based on above word blocking)
            blockPermRoll = random.randint(1,100)
            if (blockPermRoll >= random.randint(1,25)):
                random.shuffle(word_blocks)
                honeyword = "".join(word_blocks)

            permuteAnyLettersRoll = random.randint(1,100)
            if permuteAnyLettersRoll >= 65:
                for i, c in enumerate(honeyword): # permutation of individual letters
                    if c.isalpha():
                        permuteLetterRoll = random.randint(1,100)
                        if permuteLetterRoll >= 50:
                            honeyword = list(honeyword)
                            honeyword[i] = random.choice(string.ascii_letters)
                            honeyword = "".join(honeyword)

            # whole honeyword case permutation (probability 20%)
            d10roll = random.randint(1,10)
            if d10roll == 1 or d10roll == 2:
                if (random.randint(0,1) == 0):
                    honeyword = honeyword.upper()
                else:
                    honeyword = honeyword.lower()
            elif d10roll >= 9: # does case permutation (random probability)
                for c in honeyword:
                    d10roll2 = random.randint(1,10)
                    if d10roll2 > random.randint(1,10):
                        honeyword = honeyword.replace(c, c.upper())

            # number permutation (always occurs)
            for c in honeyword:
                if c.isdigit():
                    honeyword = honeyword.replace(c, str(random.randint(0,9)))

            # special character permutation
            original_mapping = "~!@#$%^&*=/?"
            new_mapping = list(original_mapping)
            random.shuffle(new_mapping)
            new_mapping = "".join(new_mapping)

            transform_to_replace = str.maketrans(original_mapping, str(new_mapping)) # set the transformation map
            honeyword = honeyword.translate(transform_to_replace) # translate the honeyword

            # duplication of sweetwords/reversal of sweetword
            d100roll = random.randint(60,100)
            if d100roll > 97:
                if(d100roll % 2 == 0): # roll for whether you are duplicating or reversing sweetword
                    if (honeyword != "") and (len(honeywords) != n - 1):
                        honeywords.append(honeyword)
                else:
                    honeyword = honeyword[::-1]

            # add the honeyword to the list
            if honeyword != "":
                honeywords.append(honeyword)

#        honeywords.append(password) # add the real password
        random.shuffle(honeywords) # shuffle so the real password is in a random position

        return honeywords

    def pformat(self, word):
        '''
        Returns the pattern of input word
        '''

        letter = 0
        punctuation = 0
        digit = 0
        for i in word:
            if i in string.ascii_letters:
                letter = 1
                continue
            if i in string.digits:
                digit = 1
                continue
            if i in string.punctuation:
                punctuation = 1
        return (letter, punctuation, digit)


    def First100RockYou(self, n, password):
        rockYou100Set = self.wholeRockYou[0:100]
        honeywords = []
        # almost 50% of the honeyword come from RockYou100 and 50% outside RockYou100, if n//2 < 100
        rockYou100 = n//2
        # if 50% of n exceed 100, we take the whole RockYou100 and some honeyword outside RockYou 100
        if rockYou100 > 100:
            honeywords += rockYou100Set
            if password in rockYou100Set:
                honeywords += self.WithOutTrainingSet(n-100, password)
            else:
                honeywords += self.WithOutTrainingSet(n-101, password)
                honeywords.append(password)
            random.shuffle(honeywords)
            return honeywords

        # if 50% of n is less than 100, we take n//2 RockYou100 into honeyword,
        # these RockYou100 should at less share some common character with the real password
        outSideRockYou100 = n - rockYou100
        passwordFormat = self.pformat(password)

        # if password in RockYou100, we need to take rockYou100-1 RockYou100 into honeyword set,
        # otherwise we need to take rockYou100 RockYou100 into the honeyword set

        # keep track of which RockYou100 is chosen
        beenchosen = {q:0 for q in range(100)}

        if password in rockYou100Set:
            endFori = rockYou100-1
            beenchosen[rockYou100Set.index(password)] = 1
        else:
            endFori = rockYou100

        i = 0
        for r in random.sample(range(100),100):
            if i == endFori:
                break
            if self.pformat(rockYou100Set[r]) == passwordFormat and rockYou100Set[r] != password:
                honeywords.append(self.wholeRockYou[r])
                i += 1
                beenchosen[r] = 1

        if i < endFori:
            for k in random.sample([j for j in beenchosen if beenchosen[j] == 0], endFori-i):
                honeywords.append(rockYou100Set[k])

        if password in rockYou100Set:
            honeywords += self.WithOutTrainingSet(outSideRockYou100, password)
        else:
            honeywords += self.WithOutTrainingSet(outSideRockYou100-1, password)
        honeywords.append(password)
        random.shuffle(honeywords)
        return honeywords


    def FullRockYou(self, n, password):
        rockYouLen = len(self.wholeRockYou)
        honeywords = []
        # almost 50% of the honeyword come from wholeRockYou and 50% outside RockYou, if n//2 < rockYouLen
        rockYouLenPicked = n//2
        # if 50% of n exceed len of the whole RockYou, we take the whole RockYou and some honeyword outside RockYou
        if rockYouLenPicked > rockYouLen:
            honeywords += self.wholeRockYou
            if password in self.wholeRockYou:
                honeywords += self.WithOutTrainingSet(n-rockYouLen, password)
            else:
                honeywords += self.WithOutTrainingSet(n-rockYouLen-1, password)
                honeywords.append(password)
            random.shuffle(honeywords)
            return honeywords

        # if 50% of n is less than rockYouLen, we take n//2 RockYou into honeyword,
        # these RockYou should at less share some common pattern with the real password
        outSideRockYou = n - rockYouLenPicked
        passwordFormat = self.pformat(password)

        # if password in RockYou, we need to take rockYouLenPicked-1 RockYou into honeyword set,
        # otherwise we need to take rockYouLenPicked RockYou into the honeyword set

        # keep track of which RockYou is chosen
        beenchosen = {q:0 for q in range(rockYouLen)}

        if password in self.wholeRockYou:
            endFori = rockYouLenPicked-1
            beenchosen[self.wholeRockYou.index(password)] = 1
        else:
            endFori = rockYouLenPicked

        i = 0
        # Pick the rockyou passwords that share the common pattern with our keywords
        for r in random.sample(range(rockYouLen), rockYouLen):
            if i == endFori:
                break
            if self.pformat(self.wholeRockYou[r]) == passwordFormat and self.wholeRockYou[r] != password:
                honeywords.append(self.wholeRockYou[r])
                i += 1
                beenchosen[r] = 1

        # If there aren't enough rockyou passwords that share the pattern, just add other passwords
        if i < endFori:
            for k in random.sample([j for j in beenchosen if beenchosen[j] == 0], endFori-i):
                honeywords.append(self.wholeRockYou[k])

        if password in self.wholeRockYou:
            honeywords += self.WithOutTrainingSet(outSideRockYou, password)
        else:
            honeywords += self.WithOutTrainingSet(outSideRockYou-1, password)
        honeywords.append(password)
        random.shuffle(honeywords)
        return honeywords


def main(argv):
    if len(sys.argv) != 4:
        print('''
        Usage:
        your_program.py n input_filename output_filename
        ''')
        return
    # parse parameter
    n = int(argv[1])
    infile = open(argv[2], 'r')
    outfile = open(argv[3], 'w')

    honeywordConverter = HoneyWord()

    for password in infile.read().splitlines():
        print('input password: ' + password)
        hwList = honeywordConverter.FullRockYou(n, password)
        print('Honeywords generated: ' + str(len(hwList)) + '\n')
        outfile.write(','.join(hwList) + '\n')


if __name__ == "__main__":
    main(sys.argv)
