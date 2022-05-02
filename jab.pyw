from lib2to3.pgen2 import driver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
import mariadb
import random

import psutil
from psutil import process_iter
from signal import SIGTERM # or SIGKILL

import tkinter as tk
from tkinter import StringVar, ttk, messagebox

import selenium.webdriver
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows

import os, sys
from pathlib import Path
import requests
import subprocess
import shutil
from datetime import date, datetime, timedelta

import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        relative_path = Path(relative_path).name
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize the default app
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "jabiott",
  "private_key_id": "5b46a1375247e152c33f88240ab1de96cd04dd2e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7LSFMoBaJKXwq\nv1VdEp6+cjEmTLW+xsvhp6Tlju7CFuAyzdHRamSqvL6/FFrfohyyZzo4GlDVU8bS\nPVKUzYKLjw5AgNCjmh2aOihWNfYqbmYWvK2j7v39VYQWjcBzyA7UCkKg+cI7J996\nj4cgH0pgjC3GwdGuSuRoZ5I5VuBPaS7UNWJi6okIce3ClVQA04SPOewcgjRbWj7t\nLVXEljVPvMavDC4MLV2TZZwmQQ5YXWkbWYhmwSULRUlu689qZmEQxj/dtlKisZFc\nEpWfmWKgQplcsxU9o+gPJPkGmwUPJeXzmOjsEPp7/qwy872VEE03tuH8gFOlO7Oq\nl3fNg+SdAgMBAAECggEAEieH7csvNGGKMgk5ydu2+ujPfJP/IsBcYQgmFb/dx4R5\nfWP6IFIt7mN9KsJaKAustd8ORgfDZFWKWLTq8BTYvxmCe94inmOh0GYoqGf2dtob\nW8Q0IUzaZLppI9je3DwAuC9AlCV1YdB1vAj0xbhTOfcOr5L39+w6qCe3hok3G2yB\nKnw/TQRFHRgNvyqbP7Dwp6eHOexu3cRwGYddQN4b+OA9aI9Kf2iOTgii+WOyhLG1\n22u2t3Tw3IHaNe21dLiScBlrGR2R5SF6OJVEFPHrvWBYeNpj3sL7fO7gGd5IN3qP\nvJE6szKGhdWKUABQ6glo2xn+XFPkLeEwbM0QDepSMQKBgQDt5keb5T/iOmVlpNut\nIPY13kdJu8DkZC9BRjDtW2f/rRLSaXe9hIHHI5vxlQyua6J+3J1CfBDf0QNb1pag\nutdyffa98QUFRNP2MBegXux8Sf5cAWdZjrNFZ0MXM57Y6VrZNW3Klzf3cTyOMshb\nIZoirA/EuyQetwqZIUBYFbRBmQKBgQDJauGuhHMrVMIC9lfpMX3ijWtCSWj6+tc6\nEHG2wQsOlzKNHmKt1rSPYpm4VvtkHhi14kjDM5Pif6P8YmOqWV8UkJnvfOf0CAwl\n/jCJG/IVJKqAM/ldRo5wHZuksu6Odyew2mbVazXvRfVHcM9XpLk0xkwjLsip5QPD\nZ5doFz6lpQKBgQCdEB/O6PfYYD15cfImx1BGGE5we6jKIOqh6bl7u5FZ1+ZJTKBl\nWwpjczsNsB4DOcS6hOS+dDKf0dqp0273BuQfDtLMbEeoRty5+N5gXss6848fJz4Y\nfoIVHCvLMaV6B/aW2RN3YYbtsrEMILLul6yvn3F5rSQXszkoCC/2971eYQKBgGgq\nK17axskBA3kOt3Y1DzpsEq1sU6uAsHAp8vUlrrc0AIO01Cm9IRIKVx9bdJVZb0QZ\nK7Iv6Wo4wrESnSKLJ7317nZJbZfp1YaMh8NQvYirtrWoq2zOwXlABq9NjkwFWXR/\n7rCuymzdDDWPJNvZp6Kgbt2/Iy2h76lN2KKPaum1AoGALdebg9J1lb5QAtk2I+wV\nil0QhJhLE2fHiVS97YuirTKBzZM7u/qDNN3SZfJv9P9QMd+vslwvMLv4OXAPjgu2\nd/AKn6jTJDf6ty7VCw69rQaevlwCVF7rDMe12l3dv6GrKsWt1rE8CRr8u6kqjsZ0\nSQ+0Wdk+p4+etBtk89k2ntQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-w0rig@jabiott.iam.gserviceaccount.com",
  "client_id": "116316514218797878181",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-w0rig%40jabiott.iam.gserviceaccount.com"
})
admin = firebase_admin.initialize_app(cred)
db = firestore.client()

# --- main ---

class JabiOTT(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        width = 160
        height = 0

        netflix_img = tk.PhotoImage(file=resource_path("images\ico_netflix.png"))
        netflix_btn = tk.Button(self, image=netflix_img, command=self.startNetflix, highlightthickness = 0, bd = 0)
        netflix_btn.pack()
        height += 50

        disney_img = tk.PhotoImage(file=resource_path("images\ico_disney.png"))
        disney_btn = tk.Button(self, image=disney_img, command=self.startDisney, highlightthickness = 0, bd = 0)
        disney_btn.pack()
        height += 50
        
        wavve_img = tk.PhotoImage(file=resource_path("images\ico_wavve.png"))
        wavve_btn = tk.Button(self, image=wavve_img, command=self.startWavve, highlightthickness = 0, bd = 0)
        wavve_btn.pack()
        height += 50

        # watcha_img = tk.PhotoImage(file=resource_path("images\ico_watcha.png"))
        # watcha_btn = tk.Button(self, image=watcha_img, command=self.startWatcha, highlightthickness = 0, bd = 0)
        # watcha_btn.pack()
        # height += 50

        # tving_img = tk.PhotoImage(file=resource_path("images\ico_tving.png"))
        # tving_btn = tk.Button(self, image=tving_img, command=self.startTving, highlightthickness = 0, bd = 0)
        # tving_btn.pack()
        # height += 50


        # coupang_img = tk.PhotoImage(file=resource_path("images\ico_coupang.png"))
        # coupang_btn = tk.Button(self, image=coupang_img, command=self.startCoupang, highlightthickness = 0, bd = 0)
        # coupang_btn.pack()
        # height += 50
        self.conn = None
        self.currentUrl = ""
        self.ip = requests.get('https://checkip.amazonaws.com').text.strip()
        self.platform = ""
        self.lastAlive = datetime.now() - timedelta(minutes=5)
        self.chromeProc = None

        self.geometry("{}x{}+{}+{}".format(width, height, self.winfo_screenwidth() - width, self.winfo_screenheight() - height - 40))
        self.overrideredirect(True)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.mainloop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            print('Mouse clicked')
            sleep(2)
            print("Navigation to: %s " % self.driver.current_url)

    def startNetflix(self):
        self.platform = "netflix"
        driver = self.runChrome("https://www.netflix.com/browse")

        accounts = db.collection(u'netflix').where(u'currentStreaming', u'<=', 4).stream()
        self.account = random.choice(list(accounts))

        sleep(2)
        r_username = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div[1]/div/label/input')
        r_username.send_keys(self.account.id)
        # driver.set_window_position(self.winfo_screenwidth(), self.winfo_height())

        r_password = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div[1]/div/label/input')
        r_password.send_keys(self.account.get("password"))
        enter = driver.find_element(by=By.XPATH, value='//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')
        
        enter.click()

        sleep(2)
        # self.chromeCenter(driver)

        # self.mouselistener = mouse.Listener(on_click=self.on_click)
        # self.mouselistener.start()


    def startDisney(self):
        self.platform = "disney"
        driver = self.runChrome("https://www.disneyplus.com/login")

        accounts = db.collection(u'disney').where(u'currentStreaming', u'<=', 4).stream()
        self.account = random.choice(list(accounts))

        r_username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # sleep(2)
        # r_username = driver.find_element(by=By.ID, value='email')

        r_username.send_keys(self.account.id)
        enter = driver.find_element(by=By.XPATH, value='//*[@id="dssLogin"]/div[1]/button')
        enter.click()
        # driver.set_window_position(self.winfo_screenwidth(), self.winfo_height())

        sleep(1)
        r_password = driver.find_element(by=By.ID, value='password')

        # r_password = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "password"))
        # )
        r_password.send_keys(self.account.get("password"))
        enter = driver.find_element(by=By.XPATH, value='//*[@id="dssLogin"]/div[1]/button')
        enter.click()
        
        sleep(3)
        # self.chromeCenter(driver)


    def startWatcha(self):
        pass
    def startTving(self):
        pass
    def startWavve(self):
        self.platform = "wavve"
        driver = self.runChrome("https://www.wavve.com/member/login")

        accounts = db.collection(u'wavve').where(u'currentStreaming', u'<=', 4).stream()
        self.account = random.choice(list(accounts))

        sleep(2)
        r_username = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/ul[1]/li[1]/label/input')
        r_username.send_keys(self.account.id)
        # driver.set_window_position(self.winfo_screenwidth(), self.winfo_height())

        r_password = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/ul[1]/li[2]/label/input')
        r_password.send_keys(self.account.get("password"))
        enter = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/div/a')
        enter.click()

        sleep(2)
        # self.chromeCenter(driver)

        pass
    def startCoupang(self):
        pass
    
    def chromeCenter(self, driver = None):
        if driver:
            driver.set_window_position((self.winfo_screenwidth() - self.chromeWidth) / 2, (self.winfo_screenheight() - self.chromeHeight) / 2)
        else:
            self.driver.set_window_position((self.winfo_screenwidth() - self.chromeWidth) / 2, (self.winfo_screenheight() - self.chromeHeight) / 2)
            
    def runChrome(self, path):
        
        process = filter(lambda p: p.name() in ["chromedriver.exe", "chrome.exe"], psutil.process_iter())
        for i in process:
            if i.pid != os.getpid():
                print(f"kill pid : {str(i.pid)} name {i.name()}")
                i.kill()
    
        # for proc in process_iter():
        #     for conns in proc.connections(kind='inet'):
        #         if conns.laddr.port == 9222:
        #             print("con", conns)
        #             try:
        #                 proc.send_signal(SIGTERM) # or SIGKILL
        #             except:
        #                 pass

        # Connect to MariaDB Platform
        if not self.conn:
            try:
                self.conn = mariadb.connect(
                    user="jabiott",
                    password="lB2]uMIasP",
                    host="jabi.us",
                    port=3307,
                    database="jabiott"

                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            # Get Cursor
            self.cur = self.conn.cursor()

        doc = db.collection(u'computers').document(u'{}'.format(self.ip))
        license = doc.get().to_dict()['license']
        expire = license.get().to_dict()['expireDate']

        if datetime.now().date() > date.fromisoformat(expire):
            messagebox.showinfo("알림", "사용 기간이 종료되었습니다. 카운터에 문의해 주세요.")
            return
        
        self.chromeWidth = 1200
        self.chromeHeight = 800

        # option = """\
        #     --chrome-frame --window-size={},{} --window-position={},{} --remote-debugging-port=9222 --user-data-dir="C:\chrometemp" --incognito --app={}\
        #     --no-displaying-insecure-content \
        #     --no-referrers \
        #     --disable-zero-suggest \
        #     --disable-sync  \
        #     --cipher-suite-blacklist=0x0004,0x0005,0xc011,0xc007""".format(self.chromeWidth, self.chromeHeight, (self.winfo_screenwidth() - self.chromeWidth) / 2, (self.winfo_screenheight() - self.chromeHeight) / 2, path)

        # chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        # if not os.path.exists(chromePath):
        #     chromePath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        #     if not os.path.exists(chromePath):
        #         chromePath = None
        #         messagebox.showinfo("알림", "브라우저 경로를 찾을 수 없습니다.")


        # try:
        #     self.chromeProc = subprocess.Popen(chromePath + " " + option, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE, shell=False, creationflags=0x08000000) # 디버거 크롬 구동
        # except:
        #     print("aaaaaaaaaaaaaaaaaaaa")
        options = Options()
        # options.add_argument("headless")
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        chrome_service = ChromeService('chromedriver')
        chrome_service.creationflags = CREATE_NO_WINDOW
        
        driver = webdriver.Chrome(options=options, service=chrome_service)
        print(path)
        driver.get(path)
        self.after(500, self.checkAlive)
        self.driver = driver
        return driver

    def checkAlive(self):
        try:
            if self.lastAlive < datetime.now() - timedelta(seconds=30):
                try: 
                    self.cur.execute("INSERT INTO online (ip,url,account,platform,latest) VALUES (?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE platform = ?, url = ?, latest = ?", (self.ip, self.currentUrl, self.account.id, self.platform, datetime.now(), self.platform, self.currentUrl, datetime.now()))
                except mariadb.Error as e: 
                    print(f"Error: {e}")
                self.conn.commit()
                self.lastAlive = datetime.now()

            if (self.currentUrl != self.driver.current_url):
                self.currentUrl = self.driver.current_url
                self.checkUrlChange()
            self.after(500, self.checkAlive)
        except WebDriverException as e:
            print("WebDriverException quit")
            self.account = None
            self.currentUrl = ""
            self.driver.quit()
        except NoSuchWindowException as e:
            print("NoSuchWindowException quit")
            self.account = None
            self.currentUrl = ""
            self.driver.quit()

    def checkUrlChange(self):
        #insert information 
        try: 
            self.cur.execute("INSERT INTO histories (ip,url,account,platform) VALUES (?, ?, ?, ?)", (self.ip, self.currentUrl, self.account.id, self.platform))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        self.conn.commit()



if __name__ == '__main__':
    app = JabiOTT()
        
