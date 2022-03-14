# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:57:11 2021

@author: talaverak1
"""
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
from time import ctime
import re
import smtplib
import requests

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening..")
        audio = r.listen(source, phrase_time_limit = 10)
    data=""
    try:
        data = r.recognize_google(audio, language='en-US')
        print("You said:"+data)
    except sr.UnknownValueError:
        print("I cannot hear you")
    except sr.RequestError as e:
        print("Request Failed")
    return data

def respond(String):
    print(String)
    tts = gTTS(text=String,lang="en")
    tts.save("Speech.mp3")
    playsound.playsound("Speech.mp3")
    os.remove("Speech.mp3")

    
def voice_assistant(data):
    if "who are you" in data:
        listening = True
        respond("I am Homer Simpson")
        
    if "how are you" in data:
        listening = True
        respond("I'm good")
        
    if "time" in data:
        listening = True
        respond(ctime())
    
    if "what is your name" in data:
        listening = True
        respond("I am Virtual Assistant")
        
    try: 
         return listen()
    except UnboundLocalError:
         print("D'oh! TimedOut-->Re-Launch")
         
        
    if "okay bye" in data:
        listening = False
        print("Listening Stopped")
        respond("See yall later")
        
time.sleep(2)
respond("Hello, What can I do for you?")  
listening = True
while listening == True:
    data = listen() #calling the listen()
    listening = voice_assistant(data)
     
    