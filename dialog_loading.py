from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import os, sys
from pathlib import Path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        relative_path = Path(relative_path).name
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoadingDialog(Toplevel):
     
    def __init__(self, master = None):
        
        super().__init__(master = master, borderwidth=0)
        self.initialize()
        self.__create_widgets()

    def initialize(self):
        self.windowWidth = 320
        self.geometry("{}x{}+{}+{}".format(self.windowWidth, 260,
         int((self.master.winfo_screenwidth() - 320) / 2), 
         int((self.master.winfo_screenheight() - 260) / 2)))

        # self.attributes("-transparentcolor", "white")
        self.config(bg='grey15')
        # just simply set window to the middle, not necessary
        # the important part, set the transparentcolor to some rare color in this case `grey15`,
        # can obvs be sth else depending on your theme
        self.attributes('-transparentcolor', 'grey15')
        # remove window from window manager
        self.overrideredirect(True)

        self.image = Image.open(resource_path(r"images/loading_bg.png"))

        self.canvas = Canvas(
            self, bg='grey15', width=self.image.width, height=self.image.height, highlightthickness=0
        )
        self.canvas.pack()

    
        # convert image to PhotoImage for `tkinter` to understand
        self.photo = ImageTk.PhotoImage(self.image)
        # put the image on canvas because canvas supports transparent bg
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.text = self.canvas.create_text(40, 220, anchor="nw", fill="white", font=('Helvetica 13 bold'))
        self.set_text("...")

    def set_text(self, text):
        try:
            self.canvas.itemconfig(self.text, text=text)
        except:
            pass
        # xOffset = self.findXCenter(self.canvas, self.text)
        # self.canvas.move(self.text, xOffset, 0)

    def findXCenter(self, canvas, item):
      coords = canvas.bbox(item)
      xOffset = (self.windowWidth / 2) - ((coords[2] - coords[0]) / 2)
      return xOffset

    def __create_widgets(self):
        print('create_widget')
        
        self.lbl = ImageLabel(self.canvas, borderwidth=0)
        self.lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.lbl.load(resource_path("images/img_loading.gif"))
        
        self.label = Label(self.canvas)

    def cancel(self):
        self.lbl.unload()
        self.destroy()
        self.update()

from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 1000

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
    
