import mysql.connector
import pyttsx3
import login_setter   # this is being used !!!!


# initializer
import speech_recognition as sr

mydb = mysql.connector.connect(host="localhost", user="root", password="69775rootpass", database="cluster")
mycur = mydb.cursor()

bot = pyttsx3.init()


def recog(tar):
    text = ""
    if tar.lower() == "name":
        i = 0
    else:
        i = 1
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
    # speak("Maybe there's some problem. Try again later.")
    # speak("Sorry for inconvenience.")
    return False


def create_table(tname):
    # mycur.execute(f'drop table if exists {user}')
    mycur.execute(f'create table {tname} (id VARCHAR(255), name VARCHAR(255), email VARCHAR(255), pass VARCHAR(255))')
    details = [["stud", "http://172.16.16.16/24online/webpages/client.jsp", "email", "pass"],
               ['codetantra', 'https://bennett.codetantra.com/login.jsp', 'email', 'pass'],
               ['lms', 'https://lms.bennett.edu.in/login/index.php', 'email', 'pass']]
    comm = ('insert into ' + tname + ' values (%s,%s,%s,%s)')
    mycur.executemany(comm, details)
    mydb.commit()


# create_table("shjjjj")


def get_details(tname, site):
    mycur.execute(f"select * from {tname} where id = '{site}'")
    details = mycur.fetchone()
    return details


def new_entry(tname, sitename, email, password):
    mycur.execute(f"update {tname} set email = '{email}', pass = '{password}' where id = '{sitename}'")
    mydb.commit()
    print("Details added successfully.")


# new_entry("shjjjj", "stud", "qwertyuisadfghjkxcvbnm", "qwsdfghjwsdfghjwsdfghj")

def get_table_data(tname):
    mycur.execute(f"select id from {tname} where email = 'email'")
    s = to_list(mycur.fetchall())
    # print(s)
    return s


def to_list(listoftup):
    if len(listoftup) == 1:
        return list(listoftup)
    tables = list(map(lambda x: list(x), listoftup))
    return list(map(lambda x: str(x)[2:-2], tables))


def speak(words):
    bot.say(words)
    bot.runAndWait()


def inputter(st):
    con = "n"
    cou = 0
    try:
        while con.lower() not in ["y", "yes", "correct", "right"] and cou != 2:
            print(f"What is your {st}?")
            speak(f"What is your {st}?")
            tname = "".join(recog(st).split())
            cou += 1
            print("Is this correct?(Yes or no)")
            speak("Is this correct?(Yes or no)")
            con = recog(tname)

        if cou > 2 or con.lower() in ["no", "n", "not"]:
            raise Exception
    except Exception:
        tname = input(f"Enter your {st} here: ").strip()
    return tname


def existing_sites(tname):
    mycur.execute(f"select id from {tname}")
    s = to_list(mycur.fetchall())
    # print(s)
    return s

def data_main(target):
    mycur.execute("show tables")
    tables = mycur.fetchall()
    tables = to_list(tables)
    print(tables)
    # target = input("Enter the task: ")
    # print(tables)
    tname = inputter("first name").lower().strip()
    if tname not in tables:
        create_table(tname)
        print("table created")
    if target not in existing_sites(tname):
        print("We currently don't have the auto login feature for this site.")
        speak("We currently don't have the auto login feature for this site.")
    else:
        if target in get_table_data(tname) :
            email = inputter("email")
            password = inputter("password")
            new_entry(tname, sitename=target, email=email, password=password)
        new_list = list(get_details(tname, target))
        exec(f"login_setter.{target}_login(*new_list)")


if __name__ == "__main__":
    data_main(input("target"))

    # ! security breaching?????

    # if not already present then make a table in the database
    # check sql
    # ----> if user already exist use that one else take new entry for first
