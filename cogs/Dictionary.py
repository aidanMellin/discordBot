from discord.ext import commands
import discord
import string
import asyncio
import requests
from dotenv import load_dotenv
from os import getenv
import simplejson
import re

from multiprocessing import Pool

load_dotenv()
DICT_API_KEY = getenv('DICT_API_KEY')

class Dictionary():
    def __init__(self):
        self.bot = None
        
    def get_data(self,word):
        try:
            req = requests.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DICT_API_KEY}')
            rJson = req.json()[0]
            print(req.json())
            print()
            syllables = rJson['hwi']['hw'].split("*")
            return syllables
        except simplejson.errors.JSONDecodeError as j:
            print(j)

    def process_input(self,sentence):
        sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()
        # sentence = [sentence[i][:-1] for i in range(len(sentence)) if sentence[i][-1] == 's']
        with Pool(5) as p:
            print(p.map(self.get_data,sentence))


if __name__ == '__main__':
    Dict = Dictionary()
    haiku = 'Haikus are hard. Sometimes they dont make sense. Refrigerator'
    # Dict.process_input("are hard Sometimes they don't make sense refrigerator")
    Dict.process_input('haikus')
