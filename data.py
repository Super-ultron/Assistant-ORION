import os
import mysql.connector
import pyttsx3
import login_setter
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)
mycur = mydb.cursor()

bot = pyttsx3.init()


def recog(tar):
    """
    Converts voice input to text.

    Args:
        tar (str): The target for which to get input ("name" or other).

    Returns:
        str: The recognized text from the user's speech.
               Returns False if speech recognition fails.
    """
    text = ""
    i = 0 if tar.lower() == "name" else 1  # Start with one retry for non-name inputs
    rec = sr.Recognizer()
    while i != 2:
        audio = ""
        with sr.Microphone() as source:
            print("speak")
            try:
                audio = rec.listen(source, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                i += 1
                continue
        print("stop")
        try:
            text = rec.recognize_google(audio)
            print("You:", text)
            return text
        except sr.UnknownValueError:
            speak("Could not understand audio, please try again.")
            print("Try to speak louder and clear :)")
            i += 1
        except sr.RequestError as e:
            speak(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )
            return False
        if text:
            break
    return False


def create_table(tname):
    """Creates a table in the database with the given name."""
    try:
        mycur.execute(
            f"CREATE TABLE IF NOT EXISTS {tname} "
            "(id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), "
            "email VARCHAR(255), pass VARCHAR(255))"
        )
        mydb.commit()
        print(f"Table {tname} created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def initialize_table(tname):
    """Initializes the table with default data."""
    try:
        details = [
            (
                "stud",
                "http://172.16.16.16/24online/webpages/client.jsp",
                "email",
                "pass",
            ),
            ("codetantra", "https://bennett.codetantra.com/login.jsp", "email", "pass"),
            ("lms", "https://lms.bennett.edu.in/login/index.php", "email", "pass"),
        ]
        comm = f"INSERT IGNORE INTO {tname} VALUES (%s, %s, %s, %s)"
        mycur.executemany(comm, details)
        mydb.commit()
        print(f"Table {tname} initialized with default data.")
    except mysql.connector.Error as err:
        print(f"Error initializing table: {err}")


def get_details(tname, site):
    """Retrieves details for a specific site from the table."""
    try:
        mycur.execute(f"SELECT * FROM {tname} WHERE id = '{site}'")
        return mycur.fetchone()
    except mysql.connector.Error as err:
        print(f"Error getting details: {err}")
        return None


def new_entry(tname, sitename, email, password):
    """Updates the email and password for a specific site in the table."""
    try:
        mycur.execute(
            f"UPDATE {tname} SET email = '{email}', pass = '{password}' "
            f"WHERE id = '{sitename}'"
        )
        mydb.commit()
        print("Details added successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating details: {err}")


def get_table_data(tname):
    """Retrieves the IDs of sites with default email from the table."""
    try:
        mycur.execute(f"SELECT id FROM {tname} WHERE email = 'email'")
        return [row[0] for row in mycur.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error getting table data: {err}")
        return []


def speak(words):
    """Converts text to speech."""
    bot.say(words)
    bot.runAndWait()


def inputter(st):
    """Gets input from the user, either through voice or keyboard."""
    con = "n"
    cou = 0
    try:
        while con.lower() not in ["y", "yes", "correct", "right"] and cou != 2:
            print(f"What is your {st}?")
            speak(f"What is your {st}?")
            tname = (
                "".join(recog(st).split()) if recog(st) else ""
            )  # Handle potential None return from recog
            cou += 1
            print("Is this correct? (Yes or no)")
            speak("Is this correct? (Yes or no)")
            con = recog(tname)

        if cou > 2 or con.lower() in ["no", "n", "not"]:
            raise ValueError("Invalid input or too many retries.")
    except (
        ValueError,
        sr.RequestError,
        TypeError,
    ) as e:  # Catch TypeError in case recog returns None
        print(f"Error: {e}")
        tname = input(f"Enter your {st} here: ").strip()
    return tname


def existing_sites(tname):
    """Retrieves the IDs of all sites in the table."""
    try:
        mycur.execute(f"SELECT id FROM {tname}")
        return [row[0] for row in mycur.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error getting existing sites: {err}")
        return []


def data_main(target):
    """Main function to handle user interaction and database operations."""
    try:
        mycur.execute("SHOW TABLES")
        tables = [row[0] for row in mycur.fetchall()]
        tname = inputter("first name").lower().strip()
        if tname not in tables:
            create_table(tname)
            initialize_table(tname)
        if target not in existing_sites(tname):
            print("We currently don't have the auto login feature for this site.")
            speak("We currently don't have the auto login feature for this site.")
            return  # Exit early if the target site is not supported

        if target in get_table_data(tname):
            email = inputter("email")
            password = inputter("password")
            new_entry(tname, sitename=target, email=email, password=password)
        new_list = get_details(tname, target)
        if new_list:
            login_func = getattr(login_setter, f"{target}_login", None)
            if login_func:
                login_func(*new_list)
            else:
                print(f"Error: Login function for {target} not found in login_setter.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    data_main(input("target: "))
