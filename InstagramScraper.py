from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
import time, re



tk = Tk()
tk['background']= '#262626'
photo = PhotoImage(file="assets/Instagram.png")
tk.iconphoto(False, photo)

# Kullanıcı bilgilerinizi buraya girin
USERNAME = Entry(tk, font=20, width=25)
PASSWORD = Entry(tk, font=20, width=25, show="*")


def Start():
    # Selenium için tarayıcıyı başlat
    driver = webdriver.Chrome()

    # Instagram'a git
    driver.get('https://www.instagram.com')

    time.sleep(2)
    usernama = USERNAME.get()
    password = PASSWORD.get()
    # Kullanıcı adı ve şifreyi gir
    username_input = driver.find_element('name', 'username')
    password_input = driver.find_element('name', 'password')

    username_input.send_keys(usernama)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)

    # Kullanıcı isimlerini kaydetmek için liste
    people_swiped = set()

    try:
        while True:
            time.sleep(5)  # 5 saniye bekleyin, manuel kaydırma için zaman verin

            userXpath = '//div[@data-testid="suggestedList"]/div[position()>1]/div/div/div[2]/div/a'

            # Örnek olarak kullanıcı isimlerini almak
            users = driver.find_elements('xpath','//a[starts-with(@href, "/") and not(contains(@href, "/explore/")) and not(contains(@href, "/direct/")) and not(contains(@href, "/p/")) and not(contains(@href, "/about/")) and string-length(@href) > 1 and not(contains(@href, "/about")) and not(contains(@href, "/reals"))]')
            for user in users:
                username = user.get_attribute('href').split('/')[-2]
                if not re.match("^[0-9]+$", username):
                    if username not in people_swiped:
                        if username != usernama:
                            people_swiped.add(username)
                            print(f"Found user: {username}")

            # Kaydedilen kullanıcı adlarını bir .txt dosyasına yaz
            with open('swiped_people.txt', 'w') as file:
                for person in people_swiped:
                    file.write(f"{person}\n")

    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
        driver.quit()
        with open('swiped_people.txt', 'w') as file:
            for person in people_swiped:
                file.write(f"{person}\n")
        print("Kullanıcı Adları Kaydedildi.")


width = "400"
height = "550"
tk.title("Instagram Scraper")
tk.geometry(f"{width}x{height}")
tk.resizable(False, False)



def show_password():
    if show_password_var.get():
        PASSWORD.config(show="")
    else:
        PASSWORD.config(show="*")

Label(text="INSTAGRAM SCRAPER", font=("Elephant", 20, "bold"), bg="#262626", fg= "#9E0707").place(x= 10, y=100)
Label(tk, text="Enter Your Instagram Name Or E_Mail", font=20, fg="white", bg="#262626").place(x=80, y= 170)
USERNAME.place(x=90, y=200)
Label(tk, text="Enter Your Instagram Password", font= 20, fg="white", bg='#262626').place(x=90, y=240)
PASSWORD.place(x= 90, y=270)
style = ttk.Style()
style.configure("Custom.TCheckbutton", background = "#262626", foreground = "white")
show_password_var = BooleanVar()
showpass = ttk.Checkbutton(tk,text="Show/Hide Password", variable=show_password_var,command=show_password, cursor="hand2", style="Custom.TCheckbutton").place(x=90, y=300)
Button(tk ,text="Start",command=Start, width=40, height=10, bg= "white", cursor="hand2").place(x=60,y=360)
Label(tk,text="By Ali Hüseyinoğlu 😉😁", font= 10, bg="#262626", fg="gold").place(x=220, y=525)
tk.mainloop()