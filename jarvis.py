#pip install speech_recognition pyaudio
#pip install setuptools
#pip install pyttsx3
# pip install pocketsphinx  #awaaaj sunta hai ye module
#pip install open ai
#pip install gtts
# pip install pygame is sy hum mp3 play kar skty hai

import speech_recognition as sr
import webbrowser
import pyttsx3
# import pocketsphinx  i am using google recognizer therefore no need
import musiclibrary
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine=pyttsx3.init()       #ye recognizer function hai jab bhi hum kuch bolengy oosko recognize karega (ye ek class hai)
newsapi="apikey"
genai.configure(api_key="apikey")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()      #ye function ek text ko lega aur oosy speak krega



def speak(text):
    tts=gTTS(text)
    tts.save('temp.mp3')

     # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def aiProcess(command):
    model = genai.GenerativeModel('gemini-2.5-flash')  # or 1.5
    response = model.generate_content(f"You are a virtual assistant. Answer briefly: {command}")
    return response.text

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")


    elif c.lower().startswith("play"):  #gana bajany ke liye function hai jo play word sun kr kaam krta hai
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)


    elif "news" in c.lower(): #ye news ka hai jo news word sunkr kaam krta hai 
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak_old(article['title'])
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak_old(output) #agar future me mainy kabhi chatgpt ki api kharidi to ye apni full power me kaam krega 
        


    if __name__ == "__main__":
        speak_old("Initialing jarvis.....")
    #listen for the wake word
    # obtain audio from the microphone

        while True:   #iss while loop ka maksad hai ki alexa sunty rhey 
            r = sr.Recognizer()
    
    # recognize speech using googleaudio
            print("recognizing....")
            try:
                with sr.Microphone() as source:
                    print("listening>>>>....")
                    audio = r.listen(source,timeout=2, phrase_time_limit=1)  #yaha listen function do chizy leta hai timeout parameter aur phase time limit parameter timeou=2 krny ke baa sirf 2 sec ke liye listen karega #phrase time limit hai ki jo chiz aapny boli hai wo kitni der aap ruks kty hai bolne ke baad

                word=r.recognize_google(audio)
                if(word.lower()=="jarvis"):
                    speak_old("ya")
            #now here after machine listen for your command
                    with sr.Microphone() as source:
                        print("alexa active>>>>>")
                        audio = r.listen(source)
                        command=r.recognize_google(audio)


                        processcommand(command)


            except Exception as e:
                print("Error; {0}".format(e))
    