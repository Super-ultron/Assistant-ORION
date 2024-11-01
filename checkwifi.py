import os
import psutil
import requests
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect():
    """Connects to the Wi-Fi network using the credentials from the .env file."""
    chromedriver = "D:\\extras\\msedgedriver.exe"  # Replace with your actual chromedriver path
    driver = webdriver.Edge(chromedriver)
    driver.get("http://172.16.16.16/24online/webpages/client.jsp")
    user = driver.find_element(By.NAME, "username")
    user.send_keys(os.getenv("WIFI_USERNAME"))  # Get username from environment variables
    password = driver.find_element(By.NAME, "password")
    password.send_keys(os.getenv("WIFI_PASSWORD"))  # Get password from environment variables
    driver.find_element(By.NAME, "login").click()
    driver.close()

def is_wifi_connected():
    """Checks if the device is connected to a Wi-Fi network."""
    try:
        # Use psutil to get a list of network interfaces
        interfaces = psutil.net_if_addrs()
        for interface_name, addresses in interfaces.items():
            # Check if the interface is a Wi-Fi interface and has a valid IPv4 address
            if "Wi-Fi" in interface_name or "Wireless" in interface_name:
                for address in addresses:
                    if address.family == psutil.AF_LINK and psutil.net_if_stats()[interface_name].isup:
                        return True
    except Exception as e:
        print(f"Error checking Wi-Fi connection: {e}")
    return False

def has_internet_connection():
    """Checks if the device has an active internet connection."""
    try:
        # Try to reach a reliable website like google.com
        response = requests.get("https://www.google.com/", timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error checking internet connection: {e}")
        return False

def is_stud():
    """Checks if the device is connected to the 'STUD' Wi-Fi network."""
    try:
        name = "STUD" # Replace with your wifi name
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode('utf-8')
        return name in data
    except Exception as e:
        print(f"Error checking Wi-Fi SSID: {e}")
        return False

if __name__ == "__main__":
    while True:
        try:
            if not has_internet_connection():
                if is_wifi_connected():
                    if is_stud():
                        connect()
            time.sleep(30)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(60)  # Wait longer before retrying in case of unexpected errors