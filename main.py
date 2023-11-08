import speech_recognition as sr
import os
import webbrowser
import openai
import datetime

def say(text):
    os.system(f"say {text}")

def greet_according_to_time():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        say("Good morning Sir")
    elif 12 <= current_hour < 17:
        say("Good afternoon Sir")
    elif 17 <= current_hour < 21:
        say("Good evening Sir")
    else:
        say("Good night Sir")

def take_command():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    print('Jarvis A.I. is starting...')
    say(greet_according_to_time)
    while True:
        print("Listening...")
        query = take_command()
        sites = [["google", "https://www.google.com"],
    ["youtube", "https://www.youtube.com"],
    ["facebook", "https://www.facebook.com"],
    ["baidu", "https://www.baidu.com"],
    ["wikipedia", "https://www.wikipedia.org"],
    ["amazon", "https://www.amazon.com"],
    ["X", "https://www.x.com"],
    ["instagram", "https://www.instagram.com"],
    ["linkedin", "https://www.linkedin.com"],
    ["netflix", "https://www.netflix.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "play music" in query:
            spotify_liked_songs_uri = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
            os.system(f"open {spotify_liked_songs_uri}")
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} and {min} minutes")
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        elif "Jarvis Quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)

