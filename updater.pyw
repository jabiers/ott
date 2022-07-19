import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.constants import BOTTOM, LEFT, RIGHT, X
import shutil, os
import psutil
import sys
import requests
import threading

class UpdaterApp(tk.Tk):

    def __init__(self, link, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("업데이트")
        self.link = link
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        self.resizable(False, False)

        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200,mode="determinate")
        self.progress.pack(fill=X)
        self.lengthText = StringVar()
        self.textLabel = ttk.Label(self, textvariable=self.lengthText)
        self.textLabel.pack(side=LEFT)

        self.statusText = StringVar()
        self.statusLabel = ttk.Label(self, textvariable=self.statusText)
        self.statusLabel.pack(side=RIGHT)
        self.bytes = 0
        self.maxbytes = 1
        self.overrideredirect(True)

        self.start()

    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 1
        self.progress["maximum"] = 1
        self.read_bytes()
        #파일 다운로드
        
        socketThread = threading.Thread(target=self.fileDownload)
        socketThread.daemon = True
        socketThread.start()
        # self.after(3000, self.fileDownload)
    
    def fileDownload(self):
        self.statusText.set("다운로드중")
        file_name = "downloading.data"
        with open(file_name, "wb") as f:
            print("Downloading %s" % file_name)
            response = requests.get(self.link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                self.maxbytes = total_length
                self.progress["maximum"] = self.maxbytes
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    self.bytes = dl
                    # self.progress["value"] = self.bytes
                    # sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    # sys.stdout.flush()
                    # print(dl, done)


        self.statusText.set("다운로드 완료")
        self.moveFile()
        
        if len(sys.argv) > 1:
            self.execApp()

        self.after(3000, self.quit)

    def moveFile(self):
        try:
            shutil.move("downloading.data", "jabiott.exe")
        except Exception as e:
            print(e)
        pass

    def execApp(self):
        os.startfile("jabiott.exe")
        self.after(1000, lambda: self.statusText.set("실행중"))

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        # self.bytes += 500
        print(self.bytes, self.maxbytes)
        self.progress["value"] = self.bytes
        self.lengthText.set(f"({self.bytes} / {self.maxbytes})")
        # if self.bytes < self.maxbytes:
        #     # read more bytes after 100 ms
        self.after(100, self.read_bytes)
        # else:
        #     pass

if __name__ == '__main__':

    process = filter(lambda p: p.name() == "jabiott.exe", psutil.process_iter())
    for i in process:
        print(i, process)
        os.system('taskkill /f /pid ' + str(i.pid)) #프로세스명을 사용한 프로세스 종료
        # if i.pid != os.getpid():
        #     print("기존 프로세스를 죽였습니다")
        #     os.system('taskkill /f /pid ' + str(i.pid)) #프로세스명을 사용한 프로세스 종료
    
    app = UpdaterApp("https://github.com/jabiers/ott/releases/download/latest/jabiott.exe")
    app.mainloop()

