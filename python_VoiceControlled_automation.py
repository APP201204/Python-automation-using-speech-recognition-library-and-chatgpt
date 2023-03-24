import requests
import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import os


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello sir, how may I help you")       


def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        SpeechToText = r.recognize_google(audio, language='en-in')
        print(f"User said: {SpeechToText}\n")

    except Exception:
        print("Say that again please...")  
        return "None"
    return SpeechToText


def request(SpeechToText):
    api_endpoint = "https://api.openai.com/v1/completions"

    api_key = os.getenv("openai_api_key")

    request_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    request_data = {
        "model": "text-davinci-003",
        "prompt": f"Write python script to {SpeechToText}. Provide only code, no text",
        "max_tokens": 500,
        "temperature": 0.5
    }

    response = requests.post(api_endpoint, headers=request_headers, json=request_data)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["text"]
        with open("output3.py", "w") as file:
            file.write(response_text)
    else:
        print(f"Request failed with status code: {str(response.status_code)}")
        
        return 0

def automate():

    python_path = "/Users/aryanpatel/miniforge3/bin/python"
    script_path = "/Users/aryanpatel/Documents/VS code/python-auto/output3.py"

    subprocess.run([python_path, script_path])

    return 0
if __name__ == "__main__":
    wishMe()
    x = True
    while x == True:
        STT = takeCommand()
        request(STT)
        automate()

        if 'the time' in STT:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif 'exit' or 'quit' in STT:
            x = False
