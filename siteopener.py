import os
import urllib.request
from urllib.request import urlopen
import webbrowser
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
mycur = mydb.cursor()

def to_list(listoftup):
    """Converts a list of tuples to a list of strings."""
    if len(listoftup) == 1:
        return list(listoftup[0])  
    return [item[0] for item in listoftup] 

def link_open(link):
    """Opens the given link in a web browser."""
    try:
        weburl = urllib.request.urlopen(link)
        url = weburl.geturl()
        webbrowser.open_new(url)
        urlopen(url=url)
    except urllib.error.URLError as e:
        print(f"Error opening URL: {e}")

def main(site_name):
    """Fetches the site URL from the database and opens it."""
    try:
        mycur.execute(f"SELECT site FROM links WHERE id = '{site_name}'")
        link = mycur.fetchone()
        if link:
            print(f"Opening {site_name}")
            link_open(link[0]) 
        else:
            print(f"Site '{site_name}' not found in the database.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    print("Enter the site you want to open:")
    try:
        mycur.execute("SELECT id FROM links")
        options = to_list(mycur.fetchall())
        if options:
            print("Your options are:", ", ".join(options)) 
            site_name = input("Select your choice: ").strip().lower()
            main(site_name)
        else:
            print("No sites found in the database.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")