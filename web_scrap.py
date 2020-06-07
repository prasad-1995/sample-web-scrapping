import requests
import html5lib
from bs4 import BeautifulSoup
import mysql.connector


def scrap(value):    
    global g_loop 
    g_loop = value
    url = "https://websites.co.in/sitemap"

    r = requests.get(url)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent,"html.parser")

    anchor = soup.find_all('a',{"rel":"noopener","style":"color: #505050;"})


    all_links=set()
    for link in anchor:
        if link.get("href") != '#':
            linkText = link.get("href")
            all_links.add(linkText)
    
    link = []
    title_data = []
    count = 0
    for i in iter(all_links):
        url = "https:"+i
        link.append(url)
        r = requests.get(url)
        htmlContent = r.content   
        soup = BeautifulSoup(htmlContent,"html.parser")
        
        title = soup.title
        title_data.append(title.string)

        count = count + 1
        if count == g_loop:
            break
    return title_data,link

def show(value):
    title_data,link = scrap(value=value)
    count = 0
    print("")
    print("scrapped data as follows : ")
    for i in range(len(title_data)):
        b = title_data[i]
        c = link[i]
        print("website_name : ",b)
        print("Link : ",c)
        print("")
        count = count + 1
        if count == g_loop:
            break

def creat_database():
    loop = g_loop
    title_data,link = scrap(value=None)
    user = input("enter user name : ")
    password = input("enter password : ")
    host = input("enter host name : ")
    port = int(input("enter port number : "))
    config = {
            "user":user,
            "password":password,
            "host":host,
            "port":port,
            }
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()    
        print("Connection status : ",conn.is_connected())

    except:
        print("unable to connect")
        

    try:
        cur.execute("create database sc_data")    
    except:
        print("Unable to create database")

    try:
        sql = "use sc_data"
        cur.execute(sql)    
    except: 
        print("unable to select db")

    try:
        sql = "create table data(url LONGTEXT,Title LONGTEXT)"
        cur.execute(sql)
        print("table created")

    except:
        print("unable to create table")

    count = 0
    cur = conn.cursor()
    for i in range(len(title_data)):
        d = link[i]
        e = title_data[i]
        try:
            sql3 = "insert into data(url,Title)VALUES(%s,%s)"
            cur.execute(sql3,(d,e))
            print("Values inserted")
            count += 1
            if count == loop:
                break
            conn.commit()

        except :
            print("uanble to create database")

    choice = input("do you want to see inserted data ??")
    if choice == "yes" or choice == "y" or choice == "YES":
        try:
            sql3 = "select * from data"
            cur.execute(sql3)
            for data in cur:
                print(data)
        except :
            print("uanble to show data")



ans = input('for scrapping website automatically press "YES" else press no : ')

if ans == "yes" or ans == "YES" or ans == 'y':
    scrap(10) 
    show(10)

    db = input("to do database related operation type yes : ")
    if db == "yes":
        creat_database()

elif ans=="no" or ans == "NO" or ans == "n":
    print("")
    no = int(input("enter number of website that you want to scrapped : "))
    if no >= 20:
        print("only less than 20 numbers of website are allowed to scrapped")
    else:
        scrap(no)
        show(no)
    
    db = input("to do database related operation type yes : ")
    if db == "yes":
        creat_database()
