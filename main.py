import threading
import time
import speech_recognition as sr
import pyttsx3
import data
import re
import webbrowser
from googlesearch import search

bot = pyttsx3.init()

def recog():
    """
    Converts voice input to text.

    Returns:
        str: The recognized text from the user's speech.
              Returns False if speech recognition fails.
    """
    text = ""
    i = 0
    rec = sr.Recognizer()
    while i != 2:
        audio = ''
        with sr.Microphone() as source:
            # rec.adjust_for_ambient_noise(source)
            print("speak")
            try:  # More specific exception handling
                audio = rec.listen(source, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                i += 1
                continue
        print('stop')
        try:
            text = rec.recognize_google(audio)
            print("You:", text)
            return text
        except sr.UnknownValueError:
            speak("Could not understand audio, please try again.")
            print("Try to speak louder and clear :)")
            i += 1
        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return False
        if text:
            break
    speak("Maybe there's some problem. Try again later.")
    speak("Sorry for inconvenience.")
    return False

def speak(words):
    """Converts text to speech."""
    bot.say(words)
    bot.runAndWait()

def openn(word):
    """
    Searches the internet for the given word and opens the first result in a new browser window.

    Args:
        word (str): The search query.
    """
    for j in search(word, tld="co.in", num=1, stop=1, pause=1):
        webbrowser.open_new(j)

if __name__ == "__main__":
    print("Hello, I am O.R.I.O.N.")
    print("What do you want me to do?")
    print("For ex: \nLogin lms\nLogin Codetantra\nOpen Youtube\nAnything you want to search...")
    print("Please speak after 'speak' command ")
    time.sleep(2)
    try:
        print("What do you want me to do?")
        speak("What do you want me to do?")
        text = recog()
        if not text:
            raise ValueError("No text recognized from speech input.")  # More specific exception
    except (ValueError, sr.RequestError) as e:  # Catch expected exceptions
        print(f"Error: {e}")
        print("What do you want me to do?")
        text = input("Enter here-->")
    task, target = None, None
    if text:
        if wants := re.search(r"(open|login|log in|logging)?([\w ]+)$", text.lower()):
            task, target = wants.groups()

        if not task or not target:
            if wants := re.search(r"([\w ]+)?(open|login|log in|logging)$", text.lower()):
                target, task = wants.groups()
        task, target = task.strip(), target.strip()
        if task == "login" and len(target.split()) == 1:
            data.data_main(target)
        else:
            try:
                t = threading.Timer(1.0, openn, args=(target,))  # Use args to pass arguments to the function
                t.start()
            except TypeError as e:
                print(f"Error opening {target}: {e}")