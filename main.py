import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import os
import webbrowser
from datetime import datetime
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth

OPENAI_API_KEY="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"
PORCUPINE_ACCESS_KEY="5EcgrAgHCFO7qawq3s5PSNBRhD7Ow6SVAofKDXaZiCJBwdcMWU2gjw=="

# Spotify credentials (replace with your actual credentials)
SPOTIFY_CLIENT_ID = "38a89f9ba6474f51bca14ba918e8daf4"
SPOTIFY_CLIENT_SECRET = "5dbff4466b974b3c9d12210919c13220"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"  # Example redirect URI

# Initialize the Spotipy client with the necessary OAuth scope for playback control
scope = 'user-modify-playback-state,user-read-playback-state,playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=scope))

def play_spotify_track(track_name, artist_name=None):
    # Search for the track with or without the artist's name
    query = f'track:{track_name}'
    if artist_name:
        query += f' artist:{artist_name}'
    results = sp.search(query, type='track', limit=1)
    tracks = results['tracks']['items']

    if tracks:
        track_uri = tracks[0]['uri']
        sp.start_playback(uris=[track_uri])  # Assuming a Spotify device is active
        say(f"Playing {track_name} by {artist_name if artist_name else 'unknown artist'}.")
    else:
        say("I couldn't find the track you requested.")

def get_spotify_recommendations(genre=None):
    results = sp.recommendations(seed_genres=[genre] if genre else None, limit=5)
    tracks = results['tracks']
    say("Here are some recommendations:")
    for track in tracks:
        say(f"{track['name']} by {track['artists'][0]['name']}")

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
        
# Global variable to maintain conversation history
conversation_history = []

def get_openai_response(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Add the latest query to the conversation history
    conversation_history.append(f"User: {query}\n")

    # Construct the prompt with the conversation history
    conversation_prompt = "".join(conversation_history[-5:])  # Use the last 5 exchanges
    conversation_prompt += "Jarvis:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=conversation_prompt,
            max_tokens=150,
            temperature=0.7,  # Adjust this to change the randomness of the responses
            stop=["User:", "Jarvis:"],  # Stop sequences for conversation
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6  # Adjust this to make the assistant more 'assertive'
        )
        
        # Extract the response text and update the conversation history
        response_text = response.choices[0].text.strip()
        conversation_history.append(f"Jarvis: {response_text}\n")

        return response_text
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def process_general_knowledge(query):
    response = get_openai_response(query)
    say(response)

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
    else:
        process_general_knowledge(query)

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
