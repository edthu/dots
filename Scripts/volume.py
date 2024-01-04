from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import subprocess
import re
import pydbus
import requests
import io


class ControlCenter:

    def __init__(self, root):
        # By default the windows closes after input. Typing "s"
        # toggles persistence
        self.destroy_after_input = True
        self.SESSION_BUS = pydbus.SessionBus()

        self.entry_style = ttk.Style()
        self.entry_style.configure("A.TEntry",
                                   fieldbackground="#363A4F",
                                   foreground="#ffffff",
                                   padding=[3, 5, 3, 5],
                                   bordercolor="#ee99a0")

        self.bg_style = ttk.Style()
        self.bg_style.configure("A.TFrame",
                                background="#292C42")

        self.label_style = ttk.Style()
        self.label_style.configure("A.TLabel", 
                                   background="#292C42",
                                   foreground="#ffffff",
                                   wraplength=200,
                                   font=("JetBrainsMono Nerd Font Mono", 12))

        self.mainframe = ttk.Frame(root,
                                   padding="5 5 5 5",
                                   width="1000",
                                   height="1000",
                                   style="A.TFrame")
        self.mainframe.grid(column=0,
                            row=0,
                            sticky=(N, W, E, S))
        """
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        """
        self.song_art = ttk.Label(self.mainframe,
                                  style="A.TLabel")

        self.information_string = StringVar()
        self.song_information = ttk.Label(
                self.mainframe,
                style="A.TLabel",
                anchor="c",
                justify="c")

        self.progress = IntVar()
        self.song_progress = ttk.Progressbar(self.mainframe,
                                             orient="horizontal",
                                             length=300,
                                             mode="determinate")

        # self.change_status()
        # self.song_progress.grid_remove()

        self.volume = StringVar(value=self.get_volume())
        current_volume = ttk.Label(self.mainframe,
                                   textvariable=self.volume,
                                   style="A.TLabel")
        current_volume.grid(row=2, column=0)

        self.input_string = StringVar()
        self.volume_entry = ttk.Entry(self.mainframe,
                                 width=10,
                                 style="A.TEntry",
                                 textvariable=self.input_string,
                                 font=("JetBrainsMono Nerd Font Mono", 12))
        self.volume_entry.grid(row=2, column=1)

        print(self.volume_entry["style"])
        print(self.volume_entry.winfo_class())
        print(self.entry_style.element_options("Entry.textarea"))
        print(self.entry_style.lookup("Entry.textarea", "font"))

        for child in self.mainframe.winfo_children():
            # grid_info = child.grid_info()
            # if grid_info["row"] != 0:
            child.grid_configure(padx=5, pady=5)
            print(child.winfo_class())

        self.change_status()
        self.volume_entry.focus()
        root.bind("<Return>", self.change_volume)

    def get_volume(self):
        sink_string = subprocess.check_output("pactl get-sink-volume 0", shell=True, text=True)
        volume = list(filter(lambda x: "%" in x, sink_string.split(" ")))[0]

        return str(volume)

    # Return album art, song, artists and album or None if there is
    # no currently playing song
    def get_data(self):
        try:
            proxy = self.SESSION_BUS.get("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
            metadata = proxy.Get("org.mpris.MediaPlayer2.Player", "Metadata")

            art_response = requests.get(metadata.get("mpris:artUrl"))
            image_bytes = io.BytesIO(art_response.content)
            pil_img = Image.open(image_bytes)
            pil_img = pil_img.resize((128, 128))
            tk_img = ImageTk.PhotoImage(pil_img)

            song = metadata.get("xesam:title")
            artists = ", ".join(metadata.get("xesam:artist"))
            album = metadata.get("xesam:album")

            return (tk_img, song, artists, album)

        except Exception as e:
            print(f"Error: {e}")
            return None

    def change_status(self):
        self.playback_data = self.get_data()
        if self.playback_data is not None:

            self.song_art["image"] = self.playback_data[0]
            self.song_art.grid(row=0, column=0)

            self.information_string.set("\n".join(self.playback_data[1:]))
            self.song_information["textvariable"] = self.information_string
            self.song_information.grid(row=0, column=1)

            print("????????")
            self.song_progress["variable"] = self.progress
            self.song_progress["mode"] = "determinate"
            self.song_progress.grid(row=1, column=0, columnspan=2)
        else:
            self.song_art.grid_remove()
            self.song_information.grid_remove()
            self.song_progress.grid_remove()

    def poll(self):
        print("ahha")
        self.change_status()
        self.volume.set(self.get_volume())
        self.volume_entry.focus()
        root.after(500, self.poll)

    """
        Function that takes the input of the user and
        changes volume of current output sink

        Control system volume
        [Int]j - Reduce volume by [Int]
        [Int]k - Increase volume by [Int]
        m      - Mute
        [Int]  - Change volume to [Int]
        q      - Close the window

        Control current audio player
        [Int]l - skip ahead [Int] seconds
        [Int]h - go back [Int] seconds
        l      - next track
        h      - previous track
        p      - toggle pause/play
    """

    def change_volume(self, *args):
        input = str(self.input_string.get())

        mute = re.fullmatch(r'm', input)
        toggle_close_after_input = re.fullmatch(r's', input)
        close = re.fullmatch(r'q', input)
        decrease = re.fullmatch(r'(\d+)j', input)
        increase = re.fullmatch(r'(\d+)k', input)
        backward = re.fullmatch(r'(\d+)h', input)
        forward = re.fullmatch(r'(\d+)l', input)
        set_volume = re.fullmatch(r'\d+', input)
        skip = re.fullmatch(r'l', input)
        last = re.fullmatch(r'h', input)
        play_pause = re.fullmatch(r'p', input)

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
            case _ if forward:
                increment = float(input.split("l")[0])
                pos = subprocess.run("playerctl position", shell=True,
                                     capture_output=True, text=True)
                num_pos = float(pos.stdout.strip())
                new_pos = num_pos + increment
                subprocess.run(f"playerctl position {new_pos}", shell=True)
            case _ if backward:
                decrement = float(input.split("h")[0])
                pos = subprocess.run("playerctl position", shell=True,
                                     capture_output=True, text=True)
                num_pos = float(pos.stdout.strip())
                new_pos = num_pos - decrement
                subprocess.run(f"playerctl position {new_pos}", shell=True)
            case _ if skip:
                subprocess.run("playerctl next", shell=True)
            case _ if last:
                subprocess.run("playerctl previous", shell=True)
            case _ if play_pause:
                subprocess.run("playerctl play-pause", shell=True)
            case _ if close:
                root.destroy()
            case _ if toggle_close_after_input:
                self.destroy_after_input = not self.destroy_after_input
            case _:
                print("Not a valid command")

        if self.destroy_after_input:
            root.destroy()
        else:
            # Update things here?
            self.change_status()
            self.volume.set(self.get_volume())
            self.input_string.set("")
            self.volume_entry.focus()

root = Tk()
cc = ControlCenter(root)
cc.poll()
root.mainloop()
