import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import os
import webbrowser
from datetime import datetime
import openai

def say(text):
    os.system(f"say '{text}'")

def greet_according_to_time():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        say("Good morning, Sir.")
    elif 12 <= current_hour < 17:
        say("Good afternoon, Sir.")
    elif 17 <= current_hour < 21:
        say("Good evening, Sir.")
    else:
        say("Good night, Sir.")

def take_command(recognizer, microphone):
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("I didn't catch that. What did you say?")
            return "None"
def get_openai_response(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or whichever model you prefer
            prompt=query,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def handle_command(query):
    sites = [
        ["google", "https://www.google.com"],
        ["youtube", "https://www.youtube.com"],
        ["facebook", "https://www.facebook.com"],
        ["baidu", "https://www.baidu.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["amazon", "https://www.amazon.com"],
        ["x", "https://www.x.com"],
        ["instagram", "https://www.instagram.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["netflix", "https://www.netflix.com"],
        # Add more sites here if needed
    ]
    
    for site in sites:
        if f"open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])
            return

    if "play music" in query.lower():
        spotify_liked_songs_uri = "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
        os.system(f"open {spotify_liked_songs_uri}")
        return

    elif "what's the time" in query.lower():
        now = datetime.now()
        say(f"Sir, the time is {now.strftime('%I:%M %p')}")
        return
    elif "what is" in query.lower() or "who is" in query.lower() or "tell me about" in query.lower():
        response = get_openai_response(query)
        say(response)
        return

    # Add more commands here if needed

# Your main function
def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Access the environment variable for the Porcupine access key
    porcupine_access_key = os.getenv('PORCUPINE_ACCESS_KEY')
    if not porcupine_access_key:
        raise EnvironmentError("The environment variable PORCUPINE_ACCESS_KEY is not set.")

    porcupine = pvporcupine.create(access_key=porcupine_access_key, keywords=["jarvis"])

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        print('Jarvis A.I. is starting...')
        greet_according_to_time()

        while True:
            try:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                if porcupine.process(pcm):
                    print("Wake word detected!")
                    command = take_command(recognizer, microphone)
                    handle_command(command)
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    # Ignore input overflow error (drop frame)
                    pass
                else:
                    raise e

    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == '__main__':
    main()
