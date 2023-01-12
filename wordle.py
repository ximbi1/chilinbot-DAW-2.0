import random

class Word():
    wordlist_five = []
    keyword = ''
    invalid_letters = []
    guesses = 0
    complete = False
    def __init__(self):
        with open('wordle.txt',mode='r') as file:
            for i in file:
                self.wordlist_five.append(i[:5])

    def generate(self):
        result = random.sample(self.wordlist_five,k=1)
        self.keyword = result[0]
        self.invalid_letters = []
        self.guesses = 0
        self.complete = 0
        return self.keyword    

    def guess(self,word):
        key = self.keyword
        key2 = self.keyword
        result = []
        count = 0
        if word not in self.wordlist_five:
            return 'no esta en la lista de palabras'
        # green and black first, then seprate loop for yellow after we replace the repeats
        for i in word:
            # green
            if i == key[count]:
                key2 = list(key2)
                key2[count] = '#'
                key2 = ''.join(key2)
                result.append('🟩')

            # yellow
            elif i in key and i != key[count]:
                result.append('🟨')
            
            # black
            elif i not in key:
                result.append('⬜')
                if i not in self.invalid_letters:
                    self.invalid_letters.append(i)

            
            count += 1
        count = 0
        #print(key2)
        for i in word:
            
            # already found
            if key2[count] == '#' or key2[count] == '*':
                pass
            # yellow
            elif i in key2 and i != key2[count]:
                # see if the similar letters were found
                result[count] = '🟨'
            elif i not in key2 and i != key[count]:
                result[count] = '⬜'
            count += 1
        result_str = ''.join(result)
        self.guesses += 1
        if result_str == '🟩🟩🟩🟩🟩':
            self.complete = True
        return result_str
'''
test = Word()
test.generate()
'''
'''
word = Word()
word.keyword = 'store'
print(word.guess('those'))'''