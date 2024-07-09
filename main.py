import threading
import time
import speech_recognition as sr
import pyttsx3
import data
# import siteopener
import re
import webbrowser
from googlesearch import search


bot = pyttsx3.init()


# converting voice to text
def recog():
    text = ""
    i = 0
    rec = sr.Recognizer()
    while i != 2:
        audio = ''
        with sr.Microphone() as source:
            # rec.adjust_for_ambient_noise(source)
            print("speak")
            audio = rec.listen(source, phrase_time_limit=5)
        print('stop')
        try:
            text = rec.recognize_google(audio)
            print("You:", text)
            return text
        except:
            speak("Could not understand audio, please try again.")
            print("Try to speak louder and clear :)")
            i += 1
        if text:
            break
    speak("Maybe there's some problem. Try again later.")
    speak("Sorry for inconvenience.")
    return False


# converting text to voice
def speak(words):
    bot.say(words)
    bot.runAndWait()


# searching and opening page on internet
def openn(word):
    for j in search(word, tld="co.in", num=1, stop=1, pause=1):
        w = webbrowser.open_new(j)


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
        if not(text):
            raise Exception
    except:
        print("What do you want me to do?")
        text = input("Enter here-->")
    task, target = None, None
    if text:
        if wants := re.search(r"(open|login|log in|logging)?([\w ]+)$", text.lower()):
            task, target = wants.groups()

        if not(task) or not(target):
            if wants := re.search(r"([\w ]+)?(open|login|log in|logging)$", text.lower()):
                target, task = wants.groups()
        task, target = task.strip(), target.strip()
        if task == "login" and len(target.split()) == 1:
            data.data_main(target)
        else:
            try:
                t = threading.Timer(1.0, openn(target))
                t.start()
            except TypeError:
                print(f"{target} opened")
