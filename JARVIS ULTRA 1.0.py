import speech_recognition as sr
import pyttsx3
import os
import random
import pyautogui
import requests
import datetime
import psutil
import ctypes
import subprocess
import time
from playsound import playsound
import threading
import signal
import pywhatkit  # for WhatsApp messaging
import pyperclip

# Personal Data (You can change it)
MY_NAME = "Praneeth"
MY_DOB = "April 23, 2013"
MY_PHONE = "+919962289144"
MY_FRIENDS = ["Aariz", "Kamalesh", "Benito", "Ajay", "Yashwanth"]
MY_MOTHER = "Geetha"
MY_FATHER = "Sudhakar"
MY_BROTHER = "Srimanth"
MY_UNCLES = ["Chakar Mam", "Srinu Lycan"]
MY_GRANNYS = ["Thirupathamal", "Rani", "Laskshmi"]
MY_GRANDPA = "Maliyadri"
MY_AUNTS = ["Akshitha", "Rekha"]

# Spotify Song Links
SPOTIFY_SONGS = [
    "https://open.spotify.com/track/6dFQ3W3xuG4ll7cNjIsN2Q?si=a648da8908474b26",
    "https://open.spotify.com/track/56zZ48jdyY2oDXHVnwg5Di?si=4d00b350423b45c7",
    "https://open.spotify.com/track/7mLEUzAulFygMchoGMrP8E?si=1067273e9d474dd8",
    "https://open.spotify.com/track/5MrLQeEVCWueDR4XejhFNG?si=8eafd808ac95410e",
    "https://open.spotify.com/track/7yk8CT3m3KI8u6DEWc3dFk?si=6d5b9d32463f439b",
    "https://open.spotify.com/track/5gBa7yfdEUKrpJbhAygKRs?si=e5375c1c14a84d08",
    "https://open.spotify.com/track/1PaxAUxLEVpi75l0nDtwu1?si=ac1ca5d52932443d",
    "https://open.spotify.com/track/2LcXJP95e4HKydTZ2mYfrx?si=fdef373baec74124"
]

# API Keys
GEMINI_API_KEY = "AIzaSyAlo9_nqpO8ESSH0vUuRzMawm6MKYDL_Vk"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
WEATHER_API_KEY = "36fc0775d3624447bb865429252804"
CITY = "Chennai"

engine = pyttsx3.init()
engine.setProperty('rate', 150)

is_listening = True

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You: {command}")
        return command
    except:
        return ""

def ask_gemini(prompt):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_URL, json=payload)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply
    except:
        return "Sorry, I couldn't fetch a response."

def take_screenshot():
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    # Find the next available screenshot number
    i = 1
    while os.path.exists(os.path.join(folder, f"screenshot {i}.png")):
        i += 1

    path = os.path.join(folder, f"screenshot {i}.png")
    pyautogui.screenshot().save(path)
    speak(f"Screenshot {i} saved.")

def lock_pc():
    speak("Locking your PC.")
    ctypes.windll.user32.LockWorkStation()

def open_youtube(): speak("Opening YouTube."); os.system("start https://www.youtube.com/")
def open_spotify(): speak("Opening Spotify."); os.system("start https://open.spotify.com/")
def open_chatgpt(): speak("Opening ChatGPT."); os.system("start https://chatgpt.com/")

def control_wifi(turn_on):
    cmd = "netsh interface set interface Wi-Fi enabled" if turn_on else "netsh interface set interface Wi-Fi disabled"
    os.system(cmd)
    speak("Wi-Fi turned on." if turn_on else "Wi-Fi turned off.")

def check_battery():
    battery = psutil.sensors_battery()
    if battery: speak(f"Battery is at {battery.percent} percent.")
    else: speak("Battery info not available.")

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no"
    try:
        data = requests.get(url).json()
        if "current" in data:
            temp = data["current"]["temp_c"]
            desc = data["current"]["condition"]["text"]
            speak(f"{CITY}'s temperature is {temp}°C with {desc}.")
        else: speak("Couldn't get weather.")
    except: speak("Weather API error.")

def system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU at {cpu} percent, RAM at {ram} percent.")

def play_music():
    song_link = random.choice(SPOTIFY_SONGS)
    speak(f"Playing your song: {song_link}")
    os.system(f"start {song_link}")

def auto_update():
    speak("Checking updates...")
    speak("Jarvis Ultra is already up to date!")

def custom_shortcut(name):
    if "vs code" in name: speak("Opening VS Code."); os.system("start code")
    elif "calculator" in name: speak("Opening Calculator."); os.system("start calc")
    elif "paint" in name: speak("Opening Paint."); os.system("start mspaint")
    else: speak("Shortcut not found.")

def control_os(command):
    if "open chrome" in command: speak("Opening Chrome."); os.system("start chrome")
    elif "open notepad" in command: speak("Opening Notepad."); os.system("start notepad")
    elif "open cmd" in command or "command prompt" in command: speak("Opening CMD."); os.system("start cmd")
    elif "shutdown computer" in command: speak("Shutting down."); os.system("shutdown /s /t 5")
    elif "restart computer" in command: speak("Restarting."); os.system("shutdown /r /t 5")
    elif "volume up" in command: speak("Volume up."); pyautogui.press('volumeup', presses=5)
    elif "volume down" in command: speak("Volume down."); pyautogui.press('volumedown', presses=5)
    elif "mute volume" in command: speak("Volume muted."); pyautogui.press('volumemute')
    elif "open settings" in command: speak("Opening Settings."); os.system("start ms-settings:")

def close_apps(command):
    apps = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "spotify": "spotify.exe",
        "calculator": "Calculator.exe",
        "vs code": "Code.exe",
        "cmd": "cmd.exe"
    }
    for app, exe in apps.items():
        if app in command:
            speak(f"Closing {app}.")
            os.system(f"taskkill /f /im {exe}")
            return

def play_intro_sound():
    try: playsound("jarvis_intro.mp3")
    except Exception as e: print(f"Intro sound error: {e}")

def handle_personal_data(command):
    if "name" in command:
        speak(f"Your name is {MY_NAME}.")
    elif "dob" in command or "date of birth" in command:
        speak(f"Your date of birth is {MY_DOB}.")
    elif "mobile number" in command or "phone number" in command:
        speak(f"Your phone number is {MY_PHONE}.")
    elif "friends" in command:
        speak("Your best friends are " + ", ".join(MY_FRIENDS))
    elif "mum" in command:
        speak(f"Your mom name is {MY_MOTHER}.")
    elif "dad" in command:
        speak(f"Your dad name is {MY_FATHER}.")
    elif "bro" in command:
        speak(f"Your bro name is {MY_BROTHER}.")
    elif "uncles" in command:
        speak("Your uncles are " + ", ".join(MY_UNCLES))
    elif "grannys" in command:
        speak("Your grannys are " + ", ".join(MY_GRANNYS))
    elif "grandpa" in command:
        speak(f"Your grandpa name is {MY_GRANDPA}.")
    elif "aunts" in command:
        speak("Your aunts are " + ", ".join(MY_AUNTS))
    else:
        speak("I don't have data on that yet.")

def send_whatsapp_message(command):
    try:
        speak("Whom should I message?")
        recipient = listen()

        if recipient == "":
            speak("I didn't catch the name.")
            return

        speak("What should I send?")
        message = listen()

        if message == "":
            speak("Message is empty.")
            return

        speak(f"Sending message to {recipient}")

        # Open WhatsApp Desktop
        os.system("start whatsapp:")

        time.sleep(5)  # Give time for app to open

        # Simulate search and sending
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.write(recipient)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(message)
        pyautogui.press('enter')

        speak("Message sent.")

    except Exception as e:
        speak("Failed to send message.")
        print("Error:", e)

def copy_to_clipboard(command):
    if "copy" in command:
        # Extract the content after 'copy' (e.g., "copy hello world to clipboard")
        text = command.replace("copy", "").replace("to clipboard", "").strip()
        if text:
            pyperclip.copy(text)
            speak(f"I've copied: {text}")
        else:
            speak("What should I copy?")

def main():
    global is_listening
    threading.Thread(target=play_intro_sound).start()
    speak("Hello! Boss,")
    
    while True:
        if not is_listening:
            time.sleep(2)
            continue

        command = listen()

        if command == "":
            continue

        if "exit" in command or "stop" in command or "goodbye" in command:
            speak("Goodbye! Have a nice day.")
            break

        if "screenshot" in command:
            take_screenshot()
        elif "lock" in command:
            lock_pc()
        elif "play music" in command:
            play_music()
        elif "weather" in command:
            get_weather()
        elif "battery" in command:
            check_battery()
        elif "system" in command:
            system_stats()
        elif "open youtube" in command:
            open_youtube()
        elif "open spotify" in command:
            open_spotify()
        elif "open chatgpt" in command:
            open_chatgpt()
        elif "update" in command:
            auto_update()
        elif "wifi" in command:
            control_wifi("on" if "on" in command else "off")
        elif "personal" in command:
            handle_personal_data(command)
        elif "whatsapp" in command:
            send_whatsapp_message(command)
        elif "copy" in command and "clipboard" in command:
            copy_to_clipboard(command)
        else:
            control_os(command)
            close_apps(command)

if __name__ == "__main__":
    main()