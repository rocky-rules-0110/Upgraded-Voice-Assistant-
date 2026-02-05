import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from datetime import datetime
import numpy as np
import random  

user_name = "friend"
voice_gender = "male"

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if voice_gender == "female":
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    else:
        engine.setProperty('voice', voices[0].id)

    engine.setProperty('rate', 150)    
    engine.say(text)
    engine.runAndWait()

def get_audio(duration=4, fs=16000):
    r = sr.Recognizer()
    try:
        print("Listening...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio_data = recording.tobytes()
        audio = sr.AudioData(audio_data, fs, 2) 
        
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("I'm sorry, I didn't catch that. Could you say it again?")
            return ""
        except sr.RequestError:
            speak("I am having trouble connecting to the recognition service.")
            return ""
    except Exception as e:
        print(f"Recording error: {e}")
    return ""

def respond_to_command(command):
    global user_name, voice_gender
    
    if "date" in command:
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")

    elif "my name is" in command:
        user_name = command.split("is")[-1].strip()
        speak(f"Nice to meet you, {user_name}!")

    elif "hello" in command:
        speak(f"Hello {user_name}! How can I help you?")

    elif "fact" in command:
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
            "A single strand of spaghetti is called a spaghetto.",
            "Octopuses have three hearts.",
            "Bananas are berries, but strawberries aren't.",
            "A day on Venus is longer than a year on Venus."
        ]
        speak(random.choice(facts))

    elif "use male voice" in command:
        voice_gender = "male"
        speak("I have switched to the male voice.")
    elif "use female voice" in command:
        voice_gender = "female"
        speak("I have switched to the female voice.")

    elif "your name" in command:
        speak("I am your smart command pro assistant.")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")
    elif "exit" in command or "quit" in command or "stop" in command:
        speak(f"Goodbye {user_name}!")
        return False
    else:
        speak("I am not sure how to help with 그hat.")
        
    return True

def main():
    speak("Assistant activated.")
    running = True
    while running:
        cmd = get_audio()
        if cmd:
            running = respond_to_command(cmd)

if __name__ == "__main__":
    main()