appVersion = "0.99.13"
# appVersion = "test"
from win32api import GetMonitorInfo, MonitorFromPoint
from enum import Enum

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")

import random

import psutil
from psutil import process_iter
from signal import SIGTERM # or SIGKILL
from PIL import Image, ImageTk

import tkinter as tk
import tkinter.font
from tkinter import BOTH, E, StringVar, ttk, messagebox

from dialog_loading import LoadingDialog
import threading

from selenium import webdriver
from time import sleep, time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, InvalidSessionIdException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from selenium.webdriver.common.keys import Keys

from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
import chromedriver_autoinstaller

import os, sys
from pathlib import Path
import requests
import subprocess
import shutil
from datetime import date, datetime, timedelta

import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

import queue
logMessages = []

class State(Enum):
    START = 0
    GETEXPIRE = 1
    RUNCHROME = 2
    WRITEID = 3
    WRITEPW = 4
    SELECTPF = 5
    DONE = 6

def log(*logStr):
    try:
        print(" ".join(logStr))
        logMessages.append("[%s] %s \n" % (datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), str(" ".join(logStr))))
    except: pass

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

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time()+self.interval
        while not self.stopEvent.wait(nextTime-time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

class JabiOTT(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        width = 285
        height = 250
        self.isWaitingClick = True
        self.driver = None
        self.loading = None
        self.currentUrl = ""
        self.ip = requests.get('https://checkip.amazonaws.com').text.strip()
        self.platform = ""
        self.lastAlive = datetime.now() - timedelta(minutes=5)
        self.chromeProc = None
        self.checkAliveInterval = None
        self.account = self.current_url = None
        self.stateMessage = ""
        self.debugMode = False

        self.geometry("{}x{}+{}+{}".format(width, height, self.winfo_screenwidth() - width - 20, self.winfo_screenheight() - height - (monitor_area[3] - work_area[3]) - 20))
        self.overrideredirect(True)
        self.resizable(False, False)
        self.config(bg="#21242d")
        self.config(bg="gray15")
        self.attributes('-transparentcolor', 'grey15')
        self.state = State.START

        self.image = Image.open(resource_path("images/bg.png"))

        log(self.image.width)
        canvas = tk.Canvas(
            self, bg='grey15', width=self.image.width, height=self.image.height, highlightthickness=0
        )
        canvas.pack(fill=BOTH, expand=tk.YES)
        # convert image to PhotoImage for `tkinter` to understand
        photo = ImageTk.PhotoImage(self.image)
        # put the image on canvas because canvas supports transparent bg
        canvas.create_image(0, 0, image=photo, anchor='nw')

        font=tk.font.Font(size=10, weight="bold")

        def openLogPopup(e):
            self.debugMode = True
            top = tk.Toplevel(self)
            top.geometry("600x285")
            logframe = tk.Frame(top)

            scrollbar = tk.Scrollbar(top)
            scrollbar.pack(in_=logframe, side="right", fill=tk.Y, expand=False)

            logBox = tk.Text(top, wrap=tk.NONE)
            logBox.pack(in_=logframe, side="left", expand=tk.TRUE, fill=tk.BOTH)
            logBox.config(state=tk.DISABLED)

            # scrollbar.config(command=self.logBox.yview)
            logBox['yscrollcommand'] = scrollbar.set

            logframe.pack(side=tk.BOTTOM, expand=tk.TRUE, fill=tk.BOTH)
            for logMessage in logMessages:
                logBox.configure(state=tk.NORMAL)
                logBox.insert(tk.END, logMessage)
                logBox.configure(state=tk.DISABLED)
                logBox.see(tk.END)


        title=tk.Label(canvas,text=f'otTV ({appVersion})', font=font, foreground="white", bg="#21242d")
        title.bind("<Double-Button-3>", openLogPopup)

        title.grid(row=0, column=0, sticky=tk.W, padx=(10, 0), ipady=15)

        # font=tk.font.Font(size=7, weight="bold")
        # version=tk.Label(canvas,text=appVersion, font=font, foreground="white", bg="#21242d")
        # version.grid(row=0, column=1, sticky=tk.W, ipady=15)

        close_img = tk.PhotoImage(file=resource_path("images\ico_close.png"))
        close_btn = tk.Button(canvas, image=close_img, command=lambda: self.destroy(), highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        close_btn.grid(row=0, column=2, sticky=tk.E)

        netflix_img = tk.PhotoImage(file=resource_path("images\ico_netflix_sm.png"))
        netflix_btn = tk.Button(canvas, image=netflix_img, command=self.startNetflix, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        netflix_btn.grid(row=1, column=0, padx=(20, 5), pady=(0, 5))

        disney_img = tk.PhotoImage(file=resource_path("images\ico_disney_sm.png"))
        disney_btn = tk.Button(canvas, image=disney_img, command=self.startDisney, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        disney_btn.grid(row=1, column=1, padx=5, pady=(0, 5))
        
        # wavve_img = tk.PhotoImage(file=resource_path("images\ico_wavve_sm.png"))
        # wavve_btn = tk.Button(canvas, image=wavve_img, command=self.startWavve, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        # wavve_btn.grid(row=1, column=2, padx=5, pady=(0, 5))
        
        watcha_img = tk.PhotoImage(file=resource_path("images\ico_watcha_sm.png"))
        watcha_btn = tk.Button(canvas, image=watcha_img, command=self.startWatcha, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        # watcha_btn.grid(row=1, column=2, padx=(20, 5), pady=5)
        watcha_btn.grid(row=1, column=2, padx=5, pady=(0, 5))

        tving_img = tk.PhotoImage(file=resource_path("images\ico_tving_sm.png"))
        tving_btn = tk.Button(canvas, image=tving_img, command=self.startTving, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        tving_btn.grid(row=2, column=0, padx=(20, 5), pady=5)

        coupang_img = tk.PhotoImage(file=resource_path("images\ico_coupang_sm.png"))
        coupang_btn = tk.Button(canvas, image=coupang_img, command=self.startCoupang, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        coupang_btn.grid(row=2, column=1, padx=5, pady=5)

        youtube_img = tk.PhotoImage(file=resource_path("images\ico_youtube.png"))
        youtube_btn = tk.Button(canvas, image=youtube_img, command=self.startYoutube, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        youtube_btn.grid(row=2, column=2, padx=5, pady=5)

        
        # apple_img = tk.PhotoImage(file=resource_path("images\ico_appletv_sm.png"))
        # apple_btn = tk.Button(canvas, image=apple_img, command=self.startApple, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        # apple_btn.grid(row=3, column=0, padx=(20, 5), pady=5)

        # b_img = tk.PhotoImage(file=resource_path("images\ico_coupang_sm.png"))
        # b_btn = tk.Button(canvas, image=b_img, command=self.startCoupang, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        # b_btn.grid(row=3, column=1, padx=5, pady=5)

        # c_img = tk.PhotoImage(file=resource_path("images\ico_youtube.png"))
        # c_btn = tk.Button(canvas, image=c_img, command=self.startYoutube, highlightthickness = 0, bd = 0, bg="#21242d", cursor="hand2")
        # c_btn.grid(row=3, column=2, padx=5, pady=5)


        res = requests.get('http://jabi.us:3333/flags?key=version').json()
        vers = res['value']
        if appVersion != vers:
            os.startfile("updater.exe start")
            return

        self.mainloop()

    def setIsWaitingClick(self, isWait):
        self.isWaitingClick = isWait

    def startNetflix(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("netflix", ))
        login.daemon = True
        login.start()

    def startDisney(self):

        # messagebox.showinfo("알림", f'디즈니플러스 서비스는 현재 유지보수 중입니다.')
        # return
    
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("disney", ))
        login.daemon = True
        login.start()
        
    def startWatcha(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("watcha", ))
        login.daemon = True
        login.start()
    
    def startTving(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("tving", ))
        login.daemon = True
        login.start()

    def startCoupang(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("coupang", ))
        login.daemon = True
        login.start()

    def startYoutube(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("youtube", ))
        login.daemon = True
        login.start()

    def startApple(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("apple", ))
        login.daemon = True
        login.start()

    def startWavve(self):
        if self.isWaitingClick:
            self.isWaitingClick = False
            self.after(5000, lambda: self.setIsWaitingClick(True))
        else:
            return
        self.after(0, self.showLoading)

        login = threading.Thread(target=self.doLogin, args=("wavve", ))
        login.daemon = True
        login.start()

    def updateMessage(self, msg = ""):
        
        if self.loading:
            if msg != "":
                message = msg
            elif self.state == State.GETEXPIRE:
                message = "만료일 가져오는중"      
            if self.state == State.RUNCHROME:
                message = "크롬 실행중"  
            elif self.state == State.WRITEID:
                message = "아이디 입력중"
            elif self.state == State.WRITEPW:
                message = "비밀번호 입력중"
            elif self.state == State.SELECTPF:
                message = "프로필 선택중"
            self.loading.set_text(message)
        else:
            log("no loding dialog")

    def doLogin(self, platform):
        log("do Login", platform)

        res = requests.get(f'http://jabi.us:3333/flags?key=onoff{platform}').json()
        value = res['value']
        
        # if value != "on":
        #     messagebox.showinfo("알림", f'{value}')
            
        #     if self.loading:
        #         self.loading.cancel()
        #         self.loading = None
        #     return

        sleep(1)
        self.platform = platform
        limit = 4
        if platform == "coupang":
            limit = 2
        elif platform == "youtube":
            limit = 100
        accounts = db.collection(self.platform).where(u'currentStreaming', u'<', limit).order_by(u'currentStreaming').stream()

        self.account = None
        tempList = []
        for account in accounts:
            print()
            # print(account.contains("disable"))
            if account.to_dict().get("disable") != True:
                tempList.append(account)
            # if ()
            # self.account = account
            # break
        print(tempList)

        self.account = random.choice(tempList)
            

        if self.account == None:
            log("there is no")
            messagebox.showinfo("알림", f'{platform} 의 모든 계정을 사용중입니다. 잠시 후 다시 이용해주세요.')
            
            if self.loading:
                self.loading.cancel()
                self.loading = None

            return

        self.state = State.RUNCHROME
        self.updateMessage()
        log(self.account.id)

        try:
            if platform == "netflix":
                self.runChrome("https://www.netflix.com/browse")
                
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="id_userLoginId"]'))
                )
                r_username.send_keys(self.account.id)

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="id_password"]')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/div/div'))
                )
                r_profile.click()
            
            if platform == "disney":
                self.runChrome("https://www.disneyplus.com/login")

                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )

                r_username.send_keys(self.account.id)
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="dssLogin"]/div[1]/button')
                enter.click()

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                r_password.send_keys(self.account.get("password"))

                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="dssLogin"]/div[1]/button')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="remove-main-padding_index"]/div/div/section/ul/div[1]/div'))
                )
                r_profile.click()

                log("profile")
                
            
            elif platform == "wavve":            
                self.runChrome("https://www.wavve.com/member/login")

                sleep(2)
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/ul[1]/li[1]/label/input'))
                )
                r_username.send_keys(self.account.id)

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/ul[1]/li[2]/label/input')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/main/div/div[1]/form/fieldset/div/a')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div/div[1]/a[1]'))
                )
                r_profile.click()
            elif platform == "watcha":            
                self.runChrome("https://watcha.com/sign_in")

                sleep(2)
                
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/main/div[1]/main/div/form/div[1]/input'))
                )
                r_username.send_keys(self.account.id)

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/main/div[1]/main/div/form/div[2]/input')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/main/div[1]/main/div/form/div[3]/button')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/main/div[1]/section/ul/li[1]/button/div[1]'))
                )
                r_profile.click()
            elif platform == "tving":            
                self.runChrome("https://user.tving.com/pc/user/otherLogin.tving?loginType=20&from=pc&rtUrl=https://www.tving.com&csite=&isAuto=false")

                sleep(2)
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="a"]'))
                )
                r_username.send_keys(self.account.id)
                sleep(1)
                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="b"]')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="doLoginBtn"]')
                enter.click()


                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="267657715"]'))
                )
                r_profile.click()                
            elif platform == "coupang":            
                self.runChrome("https://www.coupangplay.com/login")

                sleep(2)
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/form/input'))
                )
                r_username.send_keys(self.account.id)

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[2]/form/div[1]/input')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[2]/form/div[2]/button')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div[1]/div'))
                )
                r_profile.click()
                
            elif platform == "coupang":            
                self.runChrome("https://www.coupangplay.com/login")

                sleep(2)
                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/form/input'))
                )
                r_username.send_keys(self.account.id)

                self.state = State.WRITEPW
                self.updateMessage()
                r_password = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[2]/form/div[1]/input')
                r_password.send_keys(self.account.get("password"))
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[2]/form/div[2]/button')
                enter.click()

                self.state = State.SELECTPF
                self.updateMessage()
                r_profile = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div[1]/div'))
                )
                r_profile.click()
                
            elif platform == "youtube":            
                self.runChrome("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dko%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=ko&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin", True)

                sleep(2)

                self.state = State.WRITEID
                self.updateMessage()
                r_username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
                )

                r_username.send_keys(self.account.id)
                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="identifierNext"]/div/button')
                enter.click()

                sleep(2)
                
                try:
                    captcha = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="captchaimg"]'))
                    )
                    messagebox.showinfo("알림", "로그인 2차 인증을 진행해주세요.")
                    self.driver.maximize_window()
                    self.driver.set_window_position(int((self.winfo_screenwidth() - self.chromeWidth) / 2), int((self.winfo_screenheight() - self.chromeHeight) / 2))

                except Exception as e:
                    log("except")
                
                self.state = State.WRITEPW
                self.updateMessage()
                r_password = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.NAME, 'password'))
                )
                r_password.send_keys(self.account.get("password"))

                enter = self.driver.find_element(by=By.XPATH, value='//*[@id="passwordNext"]/div/button')
                enter.click()  

            elif platform == "apple":
                self.runChrome("https://tv.apple.com/kr", True)

                sleep(3)
                self.driver.implicitly_wait(15)

                self.state = State.WRITEID
                r_loginbtn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'commerce-button'))
                )

                r_loginbtn.click()
                log("id search")

                
                commerce_iframe = self.driver.find_element(By.XPATH, '//*[@id="commerce-iframe"]/iframe') #iframe 태그 엘리먼트 찾기
                self.driver.switch_to.frame(commerce_iframe) #프레임 이동

                auth_widget = self.driver.find_element(By.XPATH, '//*[@id="aid-auth-widget-iFrame"]') #iframe 태그 엘리먼트 찾기
                self.driver.switch_to.frame(auth_widget) #프레임 이동

                # self.driver.switch_to.frame(self.driver.find_elements(By.XPATH, '//*[@id="commerce-iframe"]/iframe'))

                # self.driver.execute_script(f'$("#account_name_text_field").val("{self.account.id}")')

                r_username = self.driver.find_element(By.XPATH, '//*[@id="account_name_text_field"]')

                # r_username = WebDriverWait(self.driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/apple-auth/div/div[1]/div/sign-in/div/div[1]/div[1]/div/div/div[1]/div/div/input'))
                # )

                r_username.send_keys(self.account.id)
                sleep(1)
                r_username.send_keys(Keys.RETURN)
                log("password search")

                r_password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'password_text_field'))
                )
                r_password.send_keys(self.account.get("password"))
                sleep(1)
                r_password.send_keys(Keys.RETURN)
                
            log("finish login")
            self.state = State.DONE
            self.driver.maximize_window()
            self.driver.set_window_position(int((self.winfo_screenwidth() - self.chromeWidth) / 2), int((self.winfo_screenheight() - self.chromeHeight) / 2))

        except Exception as e:
            print(e)
            log("except", str(e))

            message = ""
            if self.state == State.GETEXPIRE:
                message = f"등록되지 않은 IP({self.ip}) 입니다."  
            elif self.state == State.RUNCHROME:
                message = "크롬 실행중에 문제가 발생했습니다. 다시 선택해주세요."  
            elif self.state == State.WRITEID:
                message = "아이디 입력을 할 수 없었습니다. 다시 한번 시도해주세요."
            elif self.state == State.WRITEPW:
                message = "비밀번호를 입력 할 수 없었습니다. 다시 한번 시도해주세요."
            elif self.state == State.SELECTPF:
                message = "프로필 선택을 할 수 없었습니다. 프로필은 직접 선택하시고 시청 부탁드립니다."
                
            if self.state != State.SELECTPF:
                messagebox.showinfo("알림", message)
            else: 
                self.state = State.DONE
                self.driver.maximize_window()
                self.driver.set_window_position(int((self.winfo_screenwidth() - self.chromeWidth) / 2), int((self.winfo_screenheight() - self.chromeHeight) / 2))


        if self.loading:
            self.loading.cancel()
            self.loading = None
    
    def showLoading(self):
        if self.checkAliveInterval:
            self.checkAliveInterval.cancel()

        if self.driver:
            log("driver quit", self.driver)
            self.driver.quit()
            self.driver = None

        if self.chromeProc:
            log("chrome kill", self.chromeProc.pid)
            self.chromeProc.kill()

        if self.loading:
            self.loading.cancel()
        self.loading = LoadingDialog(self)

            
    def runChrome(self, path, proxy = False):


        self.state = State.GETEXPIRE
        # self.updateMessage()
        doc = db.collection(u'computers').document(u'{}'.format(self.ip))
        license = doc.get().to_dict()['license']
        expire = license.get().to_dict()['expireDate']
        log("expire", expire)

        if datetime.now().date() > date.fromisoformat(expire):
            messagebox.showinfo("알림", "사용 기간이 종료되었습니다. 카운터에 문의해 주세요.")
            return

        try:
            log("rmtree chrometemp")
            shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            log("except notfound")
            pass
        except PermissionError:
            log("except permission")

        
        self.chromeWidth = 1200
        self.chromeHeight = 800

        # if proxy:
        #     res = requests.get('http://jabi.us:3333/flags?key=proxyip').json()
        #     proxyIP = res['value']
        #     log("proxy server is {}".format(proxyIP))
        #     option = """--window-size={},{} --window-position={},{} --remote-debugging-port=9222 --user-data-dir="C:\chrometemp" --app={}\
        #         --proxy-server={} """.format(self.chromeWidth, self.chromeHeight, int((self.winfo_screenwidth() - self.chromeWidth) / 2), int((self.winfo_screenheight() - self.chromeHeight) / 2), path, proxyIP)
        # else:
        #     option = """--window-size={},{} --window-position={},{} --remote-debugging-port=9222 --user-data-dir="C:\chrometemp" --incognito --app={}\
        #         --no-displaying-insecure-content \
        #         --no-referrers \
        #         --disable-zero-suggest \
        #         --disable-sync  \
        #         --cipher-suite-blacklist=0x0004,0x0005,0xc011,0xc007""".format(self.chromeWidth, self.chromeHeight, int((self.winfo_screenwidth() - self.chromeWidth) / 2), int((self.winfo_screenheight() - self.chromeHeight) / 2), path)

        chromePath = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        if not os.path.exists(chromePath):
            chromePath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            if not os.path.exists(chromePath):
                chromePath = None
                messagebox.showinfo("알림", "브라우저 경로를 찾을 수 없습니다.")
        log("check ChromePath", chromePath)

        # try:
        #     info = subprocess.STARTUPINFO()
        #     if not self.debugMode:
        #         info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #         info.wShowWindow = subprocess.SW_HIDE
        #     self.chromeProc = subprocess.Popen(r"{} {}".format(chromePath, option), stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE, shell=False, creationflags=0x08000000, startupinfo=info) # 디버거 크롬 구동
        #     log("chrome open")
        # except:
        #     log("aaaaaaaaaaaaaaaaaaaa")
        options = Options()
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # options.add_experimental_option("app", path)
        options.add_argument("--incognito --app={}".format(path))
        # options.add_extension("C:\\repos\\jabi-ott\\extentions\\adblock.crx")
        try:
            driver_path = chromedriver_autoinstaller.install(True)
        except:
            log("chrome_ver fail")
            log("install fail")

        try:
            log(f"start make chromedriver {driver_path}")
            chrome_service = ChromeService(driver_path)
        except:
            chrome_service = ChromeService(resource_path('./chromedriver.exe'))
        log(chrome_service.path)
        log("made chromedriver service")
        chrome_service.creationflags = CREATE_NO_WINDOW

        try:
            self.driver = webdriver.Chrome(options=options, service=chrome_service)
        except:
            messagebox.showinfo("알림", "다시 시도해주세요.")

        log("make chrome service")
        # self.after(500, self.checkAlive)

        self.checkAliveInterval = setInterval(0.5, self.checkAlive)

        # self.driver.get(path)
        return self.driver

    
    def checkAlive(self):
        if self.driver and self.chromeProc.poll() == None:
            try:
                if (self.currentUrl != self.driver.current_url):
                    log("url", self.driver.current_url)
                    self.currentUrl = self.driver.current_url
                    self.checkUrlChange()
            except NoSuchWindowException:
                self.checkAliveInterval.cancel()
            except InvalidSessionIdException:
                self.checkAliveInterval.cancel()
            except Exception:
                self.checkAliveInterval.cancel()
        
            # self.after(500, self.checkAlive)
        else:
            log("self driver none")
            self.account = None
            self.currentUrl = ""
            self.checkAliveInterval.cancel()

        log(self.currentUrl, self.lastAlive)
        # if self.account:
        #     log('account', self.account.id)
        if self.account and self.currentUrl and self.lastAlive < datetime.now() - timedelta(seconds=30):
            try:
                requests.post('http://jabi.us:3333/online', json={
                    "ip": self.ip, 
                    "account": self.account.id, 
                    "platform": self.platform, 
                    "url": self.currentUrl
                    }, timeout=2)
                log("inserted online")
            except Exception as e:
                log(f"Error: {e}")
            self.lastAlive = datetime.now()

    def checkUrlChange(self):
        #insert information 
        if self.currentUrl.startswith("https://www.netflix.com/YourAccount") or \
            self.currentUrl.startswith("https://www.netflix.com/mfa") or \
                self.currentUrl.startswith("https://www.netflix.com/password") or \
        self.currentUrl.startswith("https://www.netflix.com/kr/loginhelp"):
            self.driver.get("https://www.netflix.com/browse")

        if self.currentUrl.startswith("https://www.netflix.com/clearcookies"):
            
        try: 
            requests.post('http://jabi.us:3333/histories', json={
                "ip": self.ip, 
                "account": self.account.id, 
                "platform": self.platform, 
                "url": self.currentUrl
                }, timeout=2)
            log("inserted")
        except Exception as e:
            log(f"Error: {e}")

if __name__ == '__main__':
    
    
    process = filter(lambda p: p.name() in ["chromedriver.exe", "chrome.exe"], psutil.process_iter())
    for i in process:
        if i.pid != os.getpid():
            log(f"kill pid : {str(i.pid)} name {i.name()}")
            i.kill()

    app = JabiOTT()
        
