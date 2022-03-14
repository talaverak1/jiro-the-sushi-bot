# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:24:28 2021

@author: kma5
"""

from gtts import gTTS
import speech_recognition as sr
import re
import time
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import requests
from pygame import mixer
import urllib.request
import urllib.parse
import bs4
import playsound
import os


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
        r.adjust_for_ambient_noise(source, duration=1)
        #listens for the user's input
        print('Homer is Ready...')
        audio = r.listen(source, phrase_time_limit = 10)
        print('analyzing...')
        
    command = ""
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = listen();

    return command

def voice_assistant():
    errors=[
        "I don't know what you mean",
        "Excuse me?",
        "Can you repeat it please?",
    ]
    "if statements for executing commands"
    
    
    while(True):
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

    #Send Email
        elif 'email' in command:
            respond('What is the subject?')
            time.sleep(3)
            subject = listen()
            respond('What should I say?')
            message = listen()
            content = 'Subject: {}\n\n{}'.format(subject, message)

        #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

        #identify to server
            mail.ehlo()

        #encrypt session
            mail.starttls()

        #login
            mail.login('your_mail', 'your_mail_password')

        #send message
            mail.sendmail('FROM', 'TO', content)

        #end mail connection
            mail.close()

            respond('Email sent.')

    
        elif 'stop' in command:
            respond("OK, see you later.")
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
            respond('Hello! I am Homer. How can I help you?')
            time.sleep(1)
        elif 'who are you' in command:
            respond('I am your assistant')
            time.sleep(1)
        else:
            error = random.choice(errors)
            respond(error)
            time.sleep(1)
        
    

respond('Homer activated!')

#loop to continue executing multiple commands
#while True:
#    time.sleep(1)
#    voice_assistant(listen())

if __name__ == '__main__':
    voice_assistant()
    