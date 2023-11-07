import speech_recognition as sr
import os

def say(text):
    os.system(f"say {text}")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ready to listen...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    return query

if __name__ == '__main__':
    print('Jarvis A.I. is starting...')
    say("Hello I am Jarvis A.I")
    while True:
        print("Listening...")
        text = take_command()
        if text != "None":
            say(text)
