# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:43:40 2021

@author: kma5
"""

from gtts import gTTS
import speech_recognition as sr
import re
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
import playsound
import os
import chatterbot.comparisons
import chatterbot.response_selection
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from Recommender_Core import d2, get_recommendations, svd




bot = ChatBot(
    'Sushi Bot',
    storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'statement_comparison_function': chatterbot.comparisons.JaccardSimilarity,
        'response_selection_method': chatterbot.response_selection.get_most_frequent_response
        }
        ],
    database_uri = 'sqlite:///database.sqlite3'
    )

trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
    "chatterbot.corpus.english.sushi",
    "chatterbot.corpus.english.sushidescriptions"
    )
#name=input("Ready")

 
    

def respond(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        tts = gTTS(text=audio, lang='en')
        tts.save("audio.mp3")
        playsound.playsound("audio.mp3")
        os.remove("audio.mp3")

        
def listen():
    "listens for commands"
    #Initialize the recognizer
    #The primary purpose of a Recognizer instance is, of course, to recognize speech. 
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 1
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source, duration=2)
        #listens for the user's input
        respond('Jiro is Ready...')
        audio = r.listen(source, phrase_time_limit = 10)
        respond('analyzing...')
        
    command = ""
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        respond('Your last command couldn\'t be heard')
        command = listen();

    return command

respond('Konichiwa, I am Jiro!')



def username():
    respond('What is your name?')
    name = listen().lower()
    respond('Hello '+ name + ' how can I help you today?')
    
    
    

def voice_assistant():
    errors=[
        "I don't know what you mean",
        "Excuse me?",
        "Can you repeat it please?",
    ]
#    "if statements for executing commands"
    
    
    while True:
    # Search on Google
        command = listen().lower()
        
        if 'open google and search' in command:
            reg_ex = re.search('open google and search (.*)', command)
            search_for = command.split("search",1)[1] 
            print(search_for)
            url = 'https://www.google.com/'
            if reg_ex:
                subgoogle = reg_ex.group(1)
                url = url + 'r/' + subgoogle
                respond('Okay!')
                driver = webdriver.Firefox(executable_path='/home/coderasha/Desktop/geckodriver')
                driver.get('http://www.google.com')
                search = driver.find_element_by_name('q')
                search.send_keys(str(search_for))
                search.send_keys(Keys.RETURN) # hit return after you enter search text


    
        elif 'stop' in command:
            respond("OK, Sayonara.")
            print("Listening Stopped")
            break
            

    # Search videos on Youtube and play (e.g. Search in youtube believer)
        elif 'youtube' in command:
            respond('Ok!')
            reg_ex = re.search('youtube (.+)', command)
            if reg_ex:
                domain = command.split("youtube",1)[1] 
                query_string = urllib.parse.urlencode({"search_query" : domain})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                #print("http://www.youtube.com/watch?v=" + search_results[0])
                webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
                pass
            
        elif 'hello' in command:
            respond('Hello! I am Sushi. How can I help you?')
            time.sleep(1)
            
        elif 'recommend' in command: 
            respond('What would you like to know?')
            command2 = listen().lower()
            if 'popular' in command2:
                respond('Here are our most popular sushis: ')
                print (d2.iloc[0]['sushi_name'] , ',', 
                   d2.iloc[1]['sushi_name'] ,', and',
                   d2.iloc[2]['sushi_name'] ,'.'
                   )
            elif 'good' in command2: 
                respond('Name a sushi you like')
                command3 = listen().lower()
                respond('Here is a list of sushi you might like')
                try: 
                    print(get_recommendations(command3))
                except: 
                    respond("I don't know that one.")
            elif 'like' in command2: 
                respond('I will find you a sushi')
                prediction = svd.predict(650001, 5, 8)
                print(prediction)
            else: 
                return
                
            
            
        elif 'who are you' in command:
            respond('I am your assistant')
            time.sleep(1)
        else:
            response = str(bot.get_response(command))
            respond(response)
            
            #error = random.choice(errors)
            #respond(error)
            time.sleep(1)
        
            


if __name__ == '__main__':
    username()
    voice_assistant()
    

    