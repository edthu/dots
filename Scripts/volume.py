from tkinter import *
from tkinter import ttk
from tkinter import font
import subprocess
import re

""""
class Mpris:

    
    Control current audio player
    [Int]l - skip ahead [Int] seconds
    [Int]h - go back [Int] seconds
    l      - next track
    h      - previous track
    p      - toggle pause/play
"""


class VolumeChanger:

    def __init__(self, root):
        self.entry_style = ttk.Style()
        self.entry_style.configure("A.TEntry", fieldbackground="#363A4F",
                                   foreground="#ffffff",
                                   padding=[3, 5, 3, 5], bordercolor="#ee99a0")
        self.bg_style = ttk.Style()
        self.bg_style.configure("A.TFrame", background="#292C42")
        self.label_style = ttk.Style()
        self.label_style.configure("A.TLabel", background="#292C42",
                                   foreground="#ffffff",font=("JetBrainsMono Nerd Font Mono", 12))

        mainframe = ttk.Frame(root, padding="5 5 5 5", width="500", height="400", style="A.TFrame")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        """
        self.sink_string = subprocess.check_output("pactl get-sink-volume 0", shell=True, text=True)
        self.volume = StringVar()
        self.volume = list(filter(lambda x: "%" in x, self.sink_string.split(" ")))[0]
        """

        self.destroy_after_input = True
        self.input_string = StringVar()
        volume_entry = ttk.Entry(mainframe, width=10, style="A.TEntry", textvariable=self.input_string, font=("JetBrainsMono Nerd Font Mono", 12))
        volume_entry.grid(column=1, row=0, sticky=(W, E))

        print(volume_entry["style"])
        print(volume_entry.winfo_class())
        print(self.entry_style.element_options("Entry.textarea"))
        print(self.entry_style.lookup("Entry.textarea", "font"))
        
        available_fonts = font.families()

        self.volume = StringVar(value=self.get_volume())
        ttk.Label(mainframe, textvariable=self.volume, style="A.TLabel").grid(column=0, row=0, sticky=(N, S, W))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        volume_entry.focus()
        root.bind("<Return>", self.change_volume)

    """
        Function that takes the input of the user and
        changes volume of current output sink

        Input string can be one of these:
        [Int]j - Reduce volume by [Int]
        [Int]k - Increase volume by [Int]
        m      - Mute
        [Int]  - Change volume to [Int]
        q      - Close the window
    """
    def get_volume(self):
        sink_string = subprocess.check_output("pactl get-sink-volume 0", shell=True, text=True)
        volume = list(filter(lambda x: "%" in x, sink_string.split(" ")))[0]
       
        return str(volume)

    def change_volume(self, *args):
        input = str(self.input_string.get())

        mute = re.fullmatch(r'm', input)
        toggle_close_after_input = re.fullmatch(r's', input)
        close = re.fullmatch(r'q', input)
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
            case _ if close:
                root.destroy()
            case _ if toggle_close_after_input:
                self.destroy_after_input = not self.destroy_after_input
            case _:
                print("Not a valid command")

        if self.destroy_after_input:
            root.destroy()
        else:
            self.volume.set(self.get_volume())
            self.input_string.set("")


root = Tk()
VolumeChanger(root)
root.mainloop()
