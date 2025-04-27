print("Script is starting...")  # Just a simple startup message

import speech_recognition as sr  # For voice recognition
import pyttsx3  # For text-to-speech
import webbrowser  # To open websites
import subprocess  # To run system commands
import requests  # To fetch data from APIs (like news)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # For AI-generated responses

# --- GUI Setup Added ---
import tkinter as tk  # For GUI window
import threading  # To run Nova and GUI together

# Setting up basic GUI window
root = tk.Tk()
root.title("Nova - AI Assistant")
root.geometry("400x500")
root.configure(bg="#1e1e2f")

status_label = tk.Label(root, text="Status: Initializing...", font=("Arial", 16), fg="white", bg="#1e1e2f")
status_label.pack(pady=20)

response_box = tk.Text(root, height=10, width=40, bg="#282c34", fg="#00ffcc", font=("Arial", 12))
response_box.pack(pady=20)
response_box.insert(tk.END, "Nova is starting...\n")
response_box.config(state="disabled")

# Functions to update GUI
def update_status(text):
    status_label.config(text=f"Status: {text}")
    root.update_idletasks()

def update_response(text):
    response_box.config(state="normal")
    response_box.insert(tk.END, f"\n{text}")
    response_box.see(tk.END)
    response_box.config(state="disabled")
    root.update_idletasks()
# --- GUI Setup Ends ---

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
    update_response(text)  # Also update the GUI box

# Function to fetch and read news aloud
def getNews():
    speak("Do you want India news or global news?")
    update_status("Waiting for news type...")  # Updating GUI status
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
        update_status("Introducing myself")
    elif "tell me about yourself" in command:
        speak("My name is Nova. My creator is Rikim Rana. My date of creation is First February 2025. and My purpose is to assist my creator. Do you need more info about me?")
        update_status("Talking about myself")
    
    # Open websites
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        update_status("Opening Google")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
        update_status("Opening Facebook")
    elif "open linkedin" in command:  
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
        update_status("Opening LinkedIn")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        update_status("Opening YouTube")
    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram")
        update_status("Opening Instagram")
    elif "open tiktok" in command:
        webbrowser.open("https://tiktok.com")
        speak("Opening TikTok")
        update_status("Opening TikTok")
    elif "open anime website" in command:
        webbrowser.open("https://hianime.to/")
        speak("Opening Anime website")
        update_status("Opening Anime Website")
    
    # Open system applications
    elif "open settings" in command:
        subprocess.run("start ms-settings:", shell=True)
        speak("Opening Settings")
        update_status("Opening Settings")
    elif "open notepad" in command:
        subprocess.run("notepad", shell=True)
        speak("Opening Notepad")
        update_status("Opening Notepad")
    elif "open word" in command:
        subprocess.run("start winword", shell=True)
        speak("Opening Word")
        update_status("Opening Word")
    elif "open excel" in command:
        subprocess.run("start excel", shell=True)
        speak("Opening Excel")
        update_status("Opening Excel")
    elif "open file explorer" in command:
        subprocess.run("explorer", shell=True)
        speak("Opening File Explorer")
        update_status("Opening File Explorer")
    elif "open calculator" in command:
        subprocess.run("calc", shell=True)
        speak("Opening Calculator")
        update_status("Opening Calculator")
    elif "open vs code" in command:
        subprocess.run("code", shell=True)
        speak("Opening VS Code")
        update_status("Opening VS Code")
    elif "open camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        speak("Opening Camera")
        update_status("Opening Camera")
    
    # Play music
    elif "play" in command and "music" in command:
        song_name = command.replace("play music", "").strip()
        if song_name:
            url = f"https://www.youtube.com/results?search_query={song_name}"
            webbrowser.open(url)
            speak(f"Playing {song_name} on YouTube")
            update_status(f"Playing {song_name}")
        else:
            speak("Which song would you like me to play?")
            update_status("Waiting for song")
    
    # AI-generated responses for anything else
    else:
        response = generate_response(command)
        print("AI:", response)
        speak(response)
        update_response(response)
        update_status("Responded")

# Main loop - listens for "Nova" and executes commands
def nova_loop():
    speak("Initializing Nova")  # Announces when Nova starts
    update_status("Waiting for Wake Word...")
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
                    update_status("Listening for Command...")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)  
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
                print("No speech detected, retrying...")
                continue

# --- Start Nova in a new thread and run the GUI ---
nova_thread = threading.Thread(target=nova_loop)
nova_thread.start()

root.mainloop()
