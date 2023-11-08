import speech_recognition as sr
import os
import webbrowser

def say(text):
    os.system(f"say {text}")

def take_command():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        # r.pause_threshold =  0.6
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
    say("Jarvis A.I")
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
