import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import checkwifi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def lms_login(id: str, site: str, email: str, pword: str):
    """Logs into the LMS website using the provided credentials."""
    try:
        driver = webdriver.Edge(os.getenv("DRIVER_PATH"))
        driver.get(site)
        user = driver.find_element(By.NAME, "username")
        user.send_keys(email)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(pword)
        driver.find_element(By.ID, "loginbtn").click()
        print("Login successful! Press Enter to close the browser.")
        input()  # Wait for user input before closing
    except Exception as e:
        print(f"An error occurred during LMS login: {e}")
    finally:
        driver.close()

def codetantra_login(id: str, site: str, email: str, pword: str):
    """Logs into the Codetantra website using the provided credentials."""
    try:
        driver = webdriver.Edge(os.getenv("DRIVER_PATH"))
        driver.get(site)
        user = driver.find_element(By.NAME, "email")
        user.send_keys(email)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(pword)
        driver.find_element(By.ID, "loginBtn").click()
        print("Login successful! Press Enter to close the browser.")
        input()  # Wait for user input before closing
    except Exception as e:
        print(f"An error occurred during Codetantra login: {e}")
    finally:
        driver.close()

def stud_login(id: str, site: str, email: str, pword: str):
    """Logs into the STUD network using the provided credentials."""
    if not checkwifi.has_internet_connection() and checkwifi.is_wifi_connected() and checkwifi.is_stud():
        try:
            driver = webdriver.Edge(os.getenv("DRIVER_PATH"))
            driver.get(site)
            user = driver.find_element(By.NAME, "username")
            user.send_keys(email)
            password = driver.find_element(By.NAME, "password")
            password.send_keys(pword)
            driver.find_element(By.NAME, "login").click()
            print("Login successful!")
        except Exception as e:
            print(f"An error occurred during STUD login: {e}")
        finally:
            driver.close()

if __name__ == "__main__":
    id = input("Enter site name: ")
    site = input("Enter site URL: ")
    email = input("Enter email: ")
    psw = input("Enter password: ")

    login_functions = {
        "lms": lms_login,
        "codetantra": codetantra_login,
        "stud": stud_login
    }
    if id in login_functions:
        login_functions[id](id, site, email, psw) 
    else:
        print("Invalid site name.")