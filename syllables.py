#Author: Aidan Mellin
'''
The primary purpose of this program is to use basic english words to try and split words based on their syllables. This can then be implemented for multiple things, including a rudimentary hypenator and a haiku generator
'''

test = "Haikus are hard. Sometimes they dont make sense. Refrigerator" #Count the number of syllables in this entry


vowels = ['a','e','i','o','u']

class Syllables():
    def __init__(self, word):
        self.word = word.lower()
        self.split_syllables = []

    def dipthong(self):
        dipthongs = ['oo','ou','ar','oi','oy','or','oo','er','ar','an','en','ir','on']
        count = 0
        # for i in range(len(self.word)):
        #     if self.word[i] in vowels and self.word[i]+self.word[i+1] in dipthongs:
        #         count += 1

        count = [i for i in range(len(self.word)) if self.word[i] in vowels and self.word[i]+self.word[i+1] in dipthongs]
        return count

    def short_vowel(self):
        pass

    def long_vowel(self):
        return [i for i in range(len(self.word)) if self.word[i] in vowels and self.word[i+1] in vowels]

    def silent_e(self):
        """
        word ends in V - C - e, e is silent
        """
        if self.word[-1] == 'e' and self.word[-3] in vowels and self.word[-2] not in vowels:
            return True

    def det_hyphen(self):
        pass

syb_generator = Syllables("mountainous")
# syb_generator = Syllables("place")

print(syb_generator.long_vowel())