"""
Created on Sat May  9 22:59:57 2020

@author: Madhan Kumar Selvaraj
"""

from flask import Flask, render_template, request
from chatbot_run import chatbot_response
from scrape import scrape_data
import speech_recognition as sr
from gtts import gTTS 
import os 
import pyttsx3
import engineio

check_wikipedia1 = ['what', 'is']
check_wikipedia2 = ['who', 'is']
check_wikihow = ['how', 'to']



def speak(text):
    language = 'en'
    output = gTTS(text=text, lang= language, slow= False)
    output.save("output.mp3")
    os.system("start output.mp3")
    
def speechtotext(text):
    x=pyttsx3.init()
    print(text)
    x.setProperty('rate',120)
    x.setProperty('volume',100)
    x.say(text)
    x.runAndAwait()


app = Flask(__name__)
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/speech")
def speech_recognition():
    r = sr.Recognizer()
    sr.pause_threshold = 0.5
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            return r.recognize_google(audio) 
        except sr.UnknownValueError:
            error = "error"
            return error

@app.route("/get")
def get_bot_response():
    user_request = request.args.get('msg')  # Fetching input from the user
    user_request = user_request.lower()
    if len(user_request.split(" ")) > 1:
        check_search = user_request.split(" ")[0]
        if check_search == 'google':
            user_request = user_request.replace("google","")
            user_request = user_request.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            check_query = user_request.split(" ")[1]
            check_text = user_request.split(" ")[1:3]
            if check_text == check_wikipedia1 or check_text == check_wikipedia2:
                response = scrape_data(user_request, "wikipedia")
            elif check_text == check_wikihow:
                response = scrape_data(user_request, "wikihow")
            elif check_query == "nearby":
                response = scrape_data(user_request, "nearby")
            else:
                response = scrape_data(user_request, "")
        else:
            if user_request == 'how are you?' or user_request == 'how are you':
                response= 'Fine , Good to see you again'
            elif user_request == 'what is your name' or user_request == 'Who are you':
                response = ' I am farmbot, I help in agriculture related problems'
            else:
                user_request = user_request.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                check_query = user_request.split(" ")[1]
                check_text = user_request.split(" ")[1:3]
                if check_text == check_wikipedia1 or check_text == check_wikipedia2:
                    response = scrape_data(user_request, "wikipedia")
                elif check_text == check_wikihow:
                    response = scrape_data(user_request, "wikihow")
                elif check_query == "nearby":
                    response = scrape_data(user_request, "nearby")
                else:
                    response = scrape_data(user_request, "")                

    else:
        if user_request == 'hi':
            response = 'Hello , Thanks for your greeting'
        elif user_request == 'bye' or  user_request == 'thankyou':
            response = 'bye, Thank you'
        elif user_request == 'hello':
            response = 'Good to see you again'
        else:
            response = 'hey'
    print(response)
    speechtotext(response)
    return response

if __name__ == "__main__":
    app.run(threaded=False)
