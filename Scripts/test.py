from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import subprocess
import re
import pydbus
import requests
import io


root = Tk()

mainframe = ttk.Frame(root)
mainframe.grid(column=1, row=1)

a = ttk.Label(mainframe, text="ayaya")
a.grid(column=2, row=0)


b = ttk.Label(mainframe, text="ayaya")
b.grid(column=1, row=0)
root.mainloop()
