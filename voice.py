import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pywhatkit
import os
import requests
import random
import tkinter as tk
from tkinter import Label, Button

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Recognize voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label.config(text="Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            label.config(text=f"You said: {command}")
            process_command(command)
        except sr.UnknownValueError:
            label.config(text="Sorry, I didn't understand.")
        except sr.RequestError:
            label.config(text="Could not connect to speech recognition service.")

# Function to process commands
def process_command(command):
    """Handles different voice commands."""
    
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")
        label.config(text=f"Time: {current_time}")

    elif "date" in command:
        today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {today_date}")
        label.config(text=f"Date: {today_date}")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        label.config(text="Opened Google")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        label.config(text="Opened YouTube")

    elif "search wikipedia for" in command:
        topic = command.replace("search wikipedia for", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
            label.config(text=result)
        except wikipedia.exceptions.DisambiguationError as e:
            label.config(text=f"Multiple results found: {e.options[:5]}")  # Showing first 5 options
        except wikipedia.exceptions.HTTPTimeoutError:
            label.config(text="Wikipedia timeout error.")
        except wikipedia.exceptions.RequestError:
            label.config(text="Wikipedia request error.")

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        label.config(text=f"Playing {song}")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "joke" in command:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet.",
            "I told my wife she should embrace her mistakes. She gave me a hug!"
        ]
        joke = random.choice(jokes)
        speak(joke)
        label.config(text=joke)

    elif "weather" in command:
        speak("Fetching weather details.")
        weather = get_weather("Pune")  # Change city as needed
        speak(weather)
        label.config(text=weather)

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.quit()

    else:
        speak("Sorry, I didn't understand that.")
        label.config(text="Command not recognized.")

# Function to fetch weather data
def get_weather(city):
    API_KEY = "your_openweathermap_api_key"  # Replace with your API key
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(URL).json()
        temperature = response["main"]["temp"]
        weather_description = response["weather"][0]["description"]
        return f"Current weather in {city}: {temperature}°C, {weather_description}"
    except:
        return "Weather information not available."

# GUI Setup
root = tk.Tk()
root.title("Advanced Voice Assistant")
root.geometry("500x350")

label = Label(root, text="Click 'Start' and Speak", font=("Arial", 14))
label.pack(pady=20)

start_button = Button(root, text="Start Listening", font=("Arial", 12), command=recognize_speech)
start_button.pack(pady=10)

exit_button = Button(root, text="Exit", font=("Arial", 12), command=root.quit)
exit_button.pack(pady=10)

speak("Hello! Click the button to start speaking.")
root.mainloop()
