# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:42:08 2021

@author: kma5
"""
import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    'Norman',
    storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'statement_comparison_function': chatterbot.comparisons.LevenshteinDistance,
        'response_selection_method': chatterbot.response_selection.get_most_frequent_response
        }
        ],
    database_uri = 'sqlite:///database.sqlite3'
    )

trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
    "chatterbot.corpus.english"
    )
name=input("Ready")
while True:
    request = input()
    if request=='Bye' or request=='bye':
        print('Bot: Bye')
        break
    else:
        response=bot.get_response(request)
        print('Bot:', response)
    
    







