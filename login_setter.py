import sys
from selenium.webdriver.common.by import By
from selenium import webdriver
import checkwifi


def lms_login(id: str, site: str, email: str, pword: str):
    # download edgedriver from https://msedgedriver.azureedge.net/108.0.1462.42/edgedriver_win64.zip
    # extract and copy its path below with '\\' instead of '\'
    edgedriver = "D:\\extras\\msedgedriver.exe"
    driver = webdriver.Edge(edgedriver)
    driver.get(site)
    user = driver.find_element(By.NAME, "username")
    user.send_keys(email)
    password = driver.find_element(By.NAME, "password")
    password.send_keys(pword)
    driver.find_element(By.ID, "loginbtn").click()
    input("Press enter to close the browser: ")
    driver.close()

def codetantra_login(id: str, site: str, email: str, pword: str):
    # download edgedriver from https://msedgedriver.azureedge.net/108.0.1462.42/edgedriver_win64.zip
    # extract and copy its path below with '\\' instead of '\'
    edgedriver = "D:\\extras\\msedgedriver.exe"
    driver = webdriver.Edge(edgedriver)
    driver.get(site)
    user = driver.find_element(By.NAME, "email")
    user.send_keys(email)
    password = driver.find_element(By.NAME, "password")
    password.send_keys(pword)
    driver.find_element(By.ID, "loginBtn").click()
    input("Press enter to close the browser: ")
    driver.close()

def stud_login(id: str, site: str, email: str, pword: str):
    # download edgedriver from https://msedgedriver.azureedge.net/108.0.1462.42/edgedriver_win64.zip
    # extract and copy its path below with '\\' instead of '\'
    if not(checkwifi.has_internet_connection()):
        if checkwifi.is_wifi_connected():
            pass
            # print("Wi-Fi is connected")
            if checkwifi.is_stud():
                edgedriver = "D:\\extras\\msedgedriver.exe"
                driver = webdriver.Edge(edgedriver)
                driver.get(site)
                user = driver.find_element(By.NAME, "username")
                user.send_keys(email)
                password = driver.find_element(By.NAME, "password")
                password.send_keys(pword)
                driver.find_element(By.NAME, "login").click()
                driver.close()
                sys.exit()


if __name__ == "__main__":
    id = input("name site")
    site = input("site")
    email = input("email")
    psw = input("pswd")
    exec(f"{id}_login(id,site,email,psw)")
