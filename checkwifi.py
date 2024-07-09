import psutil
from psutil import AF_LINK
import requests
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium import webdriver

def connect():
    chromedriver = "D:\\extras\\msedgedriver.exe"
    driver = webdriver.Edge(chromedriver)
    driver.get("http://172.16.16.16/24online/webpages/client.jsp")
    user = driver.find_element(By.NAME, "username")
    user.send_keys("E22CSEU0788@bennett.edu.in")

    password = driver.find_element(By.NAME, "password")
    password.send_keys("Bennett@#8929342373")
    driver.find_element(By.NAME, "login").click()

    driver.close()


def is_wifi_connected():
    # Get the list of all network interfaces
    interfaces = psutil.net_if_addrs()
    for interface in interfaces:
        # Check if the interface is a Wi-Fi interface
        if "Wi-Fi" in interface or "Wireless" in interface:
            # Get the list of addresses associated with the interface
            addresses = interfaces[interface]
            # Iterate through the list of addresses
            for address in addresses:
                # Check if the address is a valid IPv4 address
                if address.family == psutil.AF_LINK:
                    # Return True if the interface is up and has a valid IPv4 address
                    if psutil.net_if_stats()[interface].isup:
                        return True
    # Return False if no Wi-Fi interface was found or if the Wi-Fi interface was not up
    return False


def has_internet_connection():
    try:
        # Send an HTTP request to a website and check if the request is successful
        response = requests.get("https://www.youtube.com/")
        if response.status_code == 200:
            return True
    except:
        pass
    return False


def is_stud():
    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    data = wifi.decode('utf-8')
    # print(data)
    if "STUD" in data:
        # print("connected to stud wi-fi")
        return True
    else:
        # print("not connected to stud wi-fi")
        return False


if __name__ == "__main__":
    while True:
        if not(has_internet_connection()):
            if is_wifi_connected():
                pass
                # print("Wi-Fi is connected")
                if is_stud():
                    connect()
        time.sleep(30)








