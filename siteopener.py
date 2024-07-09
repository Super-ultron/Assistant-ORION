import urllib.request
from urllib.request import urlopen
import webbrowser
import mysql.connector


def to_list(listoftup):
    if len(listoftup) == 1:
        return list(listoftup)
    tables = list(map(lambda x: list(x), listoftup))
    return list(map(lambda x: str(x)[2:-2], tables))


def link_open(link):
    weburl = urllib.request.urlopen(link)
    url = weburl.geturl()
    webbrowser.open_new(url)
    urlopen(url=url)


def main(site_name):
    mycur.execute(f"select site from links where id = '{site_name}'")
    link = mycur.fetchone()
    # print(link)
    print(f"opening {site_name}")
    link_open(*to_list(link))


mydb = mysql.connector.connect(host="localhost", user="root", password="69775rootpass", database="cluster")
mycur = mydb.cursor()

if __name__ == "__main__":
    print("enter the site you want to open: ")
    print('your options are:')
    mycur.execute("select id from links ")
    opt = mycur.fetchall()
    print(to_list(opt))
    main(input("select your choice: ").strip().lower())
