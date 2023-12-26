from tkinter import *
from tkinter import ttk
import subprocess
import re

"""
    Function that takes the input of the user and changes
    Input string can be one of these:
    [Int]j - Reduce volume by [Int]
    [Int]k - Increase volume by [Int]
    m      - Mute
    [Int]  - Change volume to [Int]
"""

def change_volume(*args):
    input = str(input_string.get())

    mute = re.fullmatch(r'm', input)
    decrease = re.fullmatch(r'(\d+)j', input)
    increase = re.fullmatch(r'(\d+)k', input)
    set_volume = re.fullmatch(r'\d+', input)


    match input:
        case _ if mute:
            subprocess.run("pactl set-sink-mute 0 toggle", shell=True)
        case _ if decrease:
            decrement = input.split("j")[0]
            subprocess.run("pactl set-sink-volume 0 -" + decrement + "%", shell=True)
        case _ if increase:
            increment = input.split("k")[0]
            subprocess.run("pactl set-sink-volume 0 +" + increment + "%", shell=True)
        case _ if set_volume:
            subprocess.run("pactl set-sink-volume 0 " + input + "%", shell=True)
        case _:
            print("Not a valid command")

    root.destroy()

root = Tk()

mainframe = ttk.Frame(root, padding="1 1 12 12", width="500", height="300")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sink_string = subprocess.check_output("pactl get-sink-volume 0", shell=True, text=True)
print(sink_string)
volume = list(filter(lambda x: "%" in x, sink_string.split(" ")))[0]

input_string = StringVar()

volume_entry = ttk.Entry(mainframe, width=20, textvariable=input_string)
volume_entry.grid(column=1, row=0, sticky=(W, E))

ttk.Label(mainframe, text=volume).grid(column=0, row=0, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

volume_entry.focus()
root.bind("<Return>", change_volume)

root.mainloop()
