# Here is the complete code file for your AARYA Voice-Controlled AI Assistant module. You can copy this into a .py file (e.g., AARYA_Module.py) and run it on your Raspberry Pi.

# Complete Code: AARYA_Module.py


import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
import requests
import json

# Set your OpenAI API key
OPENAI_API_KEY = 'your-openai-api-key-here'

# Function to respond with the current time
def get_time():
    current_time = time.strftime("%I:%M %p")
    return f"The current time is {current_time}"

# Function to convert text to speech and play it
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts_file = "response.mp3"
    tts.save(tts_file)
    playsound.playsound(tts_file)
    os.remove(tts_file)

# Function to communicate with ChatGPT API for general queries
def send_instruction_to_chatgpt(instruction):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are AARYA, an AI assistant designed by Mandeep Singh Pawar."},
            {"role": "user", "content": instruction}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        response_data = response.json()
        reply = response_data['choices'][0]['message']['content']
        return reply
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to listen for voice commands
def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command recognized: {command}")
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Sorry, I couldn't process the request."

# Main function to detect the wake word and process the commands
def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    while True:
        print("Say 'AARYA' to activate.")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            wake_word = recognizer.recognize_google(audio).lower()
            if "aarya" in wake_word:
                print("Wake word detected! Listening for command...")
                
                # Default introduction if the command is an introduction query
                command = listen_for_command()
                if "introduce yourself" in command.lower():
                    intro = "Hello, I am AARYA. I work on AI modules designed by Mandeep Singh Pawar."
                    speak_text(intro)
                
                # Check if the command asks for time
                elif "time" in command.lower():
                    time_reply = get_time()
                    speak_text(time_reply)
                
                # Fancy welcome message for known commands
                elif "what can you do" in command.lower():
                    features = ("Hello! I am AARYA, your personal AI assistant. I can help you with tasks such as telling the time, "
                                "answering technical queries, and more. Ask me anything!")
                    speak_text(features)
                
                # For all other queries, pass them to ChatGPT
                else:
                    gpt_reply = send_instruction_to_chatgpt(command)
                    speak_text(gpt_reply)
                    
        except sr.UnknownValueError:
            pass

if __name__ == "__main__":
    main()


# Steps to Use:
# 1. Replace API Key: Update the OPENAI_API_KEY with your OpenAI API key.

# 2. Install Dependencies: Run the following commands to install the required Python libraries:

# > pip install SpeechRecognition pyaudio gtts playsound requests

# 3. Run the Script: Run the script using Python 3:

# > python3 AARYA_Module.py

# How It Works:
# Wake Word Detection:

# AARYA listens for the wake word "AARYA" using the microphone.
# When the wake word is detected, it listens for the command.
# Preset Commands:

# If you say, "introduce yourself," AARYA responds with: "Hello, I am AARYA. I work on AI modules designed by Mandeep Singh Pawar."
# If you ask, "What can you do?" it provides a list of its capabilities.
# If you ask for the time, it will give the current time.
# ChatGPT Integration:

# For any other query, AARYA will communicate with ChatGPT via the OpenAI API and provide a dynamic response.
# This module now has voice-based interactions for both preset commands and dynamic responses from the OpenAI GPT model.
