print("Script is starting...")  # Just a simple startup message

import speech_recognition as sr  # For voice recognition
import pyttsx3  # For text-to-speech
import webbrowser  # To open websites
import subprocess  # To run system commands
import requests  # To fetch data from APIs (like news)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # For AI-generated responses

# Function to generate AI-based responses using FLAN-T5 model
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Setting up the recognizer and text-to-speech engine
recognizer = sr.Recognizer()                    
engine = pyttsx3.init()

# API key for fetching news
newsapi = "91bfd3060223460daafd0d6b4ba780ed"  

# Load the AI model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to make Nova speak
def speak(text):
    engine.stop()  
    engine.say(text)
    engine.runAndWait()

# Function to fetch and read news aloud
def getNews():
    speak("Do you want India news or global news?")
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjusts for background noise
            print("Listening for news type...")
            try:
                # Listening for user's response
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                news_type = recognizer.recognize_google(audio).strip().lower()
                print("Recognized news type:", news_type)
                
                # Determining which news to fetch
                if "india" in news_type:
                    country_code = "in"  
                    params = {"country": country_code, "apiKey": newsapi}
                elif "global" in news_type:
                    params = {"category": "general", "apiKey": newsapi}  
                else:
                    speak("Sorry, I didn't understand. Please say India or global.")
                    continue  
                
                # Fetching news from API
                url = "https://newsapi.org/v2/top-headlines"
                response = requests.get(url, params=params)
                data = response.json()

                # Checking if the response is successful
                if response.status_code == 200:
                    articles = data.get("articles", [])  
                    if articles:
                        print("\nTop News Headlines:\n")
                        for index, article in enumerate(articles[:10], start=1):  # Reading top 10 news
                            print(f"{index}. {article['title']}")
                            speak(article['title'])
                    else:
                        print("No news found.")
                        speak("No news found.")
                else:
                    print(f"Error: {data.get('message', 'Failed to fetch news')}")
                    speak("Failed to fetch news.")
                break  
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                speak("Check your internet connection.")
                break
            except sr.WaitTimeoutError:
                speak("I didn't hear anything. Please try again.")

# Function to process user commands
def processCommand(command):
    command = command.strip().lower()
    
    # Basic self-introduction responses
    if "who are you" in command or "what is your name" in command:
        speak("I am Nova, your personal AI assistant.")
    elif "tell me about yourself" in command:
        speak("My name is Nova. My creator is Rikim Rana. My date of creation is First February 2025. and My purpose is to assist my creator. Do you need more info about me?")
    
    # Open websites
    elif "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command:  
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
    elif "open tiktok" in command:
        webbrowser.open("https://tiktok.com")
    elif "open anime website" in command:
        webbrowser.open("https://hianime.to/")
    
    # Open system applications
    elif "open settings" in command:
        subprocess.run("start ms-settings:", shell=True)
    elif "open notepad" in command:
        subprocess.run("notepad", shell=True)
    elif "open word" in command:
        subprocess.run("start winword", shell=True)
    elif "open excel" in command:
        subprocess.run("start excel", shell=True)
    elif "open file explorer" in command:
        subprocess.run("explorer", shell=True)
    elif "open calculator" in command:
        subprocess.run("calc", shell=True)
    elif "open vs code" in command:
        subprocess.run("code", shell=True)
    elif "open camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)
    
    # AI-generated responses for anything else
    else:
        response = generate_response(command)
        print("AI:", response)
        speak(response)

# Main loop - listens for "Nova" and executes commands
if __name__ == "__main__":
    speak("Initializing Nova")  # Announces when Nova starts
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)  # Adjusts for background noise
            try:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio).strip().lower()  
                print("Recognized wake word:", word)  
                
                # If wake word "Nova" is detected, listen for the actual command
                if "nova" in word:  
                    speak("Yaa")  # Responds when activated
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)  
                        print("Listening for command...")
                        audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
                        command = recognizer.recognize_google(audio).strip().lower()
                        
                        if len(command) < 3:
                            speak("I didn't catch that, please repeat.")
                            continue
                        
                        print("Recognized command:", command)  
                        processCommand(command)  # Process the command
            except sr.UnknownValueError:
                print("Could not understand audio")
                speak("Sorry, I didn't catch that.")
            except sr.RequestError:
                print("Check your internet connection")
                speak("Check your internet connection.")
            except sr.WaitTimeoutError:
                print("No speech detected, retrying...")  # Keeps listening if nothing is detected
