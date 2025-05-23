from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageChops
import subprocess
import re
import pydbus
import requests
import io
from threading import Thread


class ControlCenter:

    def __init__(self, root):
        # By default the windows closes after input. Typing "s"
        # toggles persistence
        self.destroy_after_input = True
        self.SESSION_BUS = pydbus.SessionBus()

        self.entry_style = ttk.Style()
        self.entry_style.configure("A.TEntry",
                                   fieldbackground="#363A4F",
                                   bordercolor="#ffffff",
                                   foreground="#ffffff",
                                   padding=[3, 5, 3, 5],
                                   # troughcolor="#363A4F",
                                   borderwidth=0,
                                   #lightcolor="#ffffff",
                                   #darkcolor="#ffffff",
                                   relief="solid")

        self.bg_style = ttk.Style()
        self.bg_style.configure("A.TFrame",
                                background="#292C42")

        self.progressbar_style = ttk.Style()
        self.progressbar_style.configure("Horizontal.TProgressbar",
                                         background="#8AADF4",
                                         troughcolor="#363A4F",
                                         #darkcolor="#363A4F",
                                         #lightcolor="#363A4F",
                                         troughrelief="flat")

        self.label_style = ttk.Style()
        self.label_style.configure("A.TLabel", 
                                   background="#292C42",
                                   foreground="#ffffff",
                                   wraplength=200,
                                   font=("JetBrainsMono Nerd Font Mono", 12))

        self.playerframe = ttk.Frame(root,
                                   padding="5 5 5 5",
                                   width="1000",
                                   height="1000",
                                   style="A.TFrame")

        self.mainframe = ttk.Frame(root,
                                   padding="5 5 5 5",
                                   width="1000",
                                   height="1000",
                                   style="A.TFrame")

        self.playerframe.grid(column=0,
                              row=0,
                              sticky=(N,W,E,S))

        self.mainframe.grid(column=0,
                            row=1,
                            sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=0)
        root.columnconfigure(2, weight=2)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=0)


        self.volume = StringVar(value=self.get_volume())
        current_volume = ttk.Label(self.mainframe,
                                   textvariable=self.volume,
                                   style="A.TLabel")
        current_volume.grid(row=2, column=0, columnspan=2)

        self.input_string = StringVar()
        self.volume_entry = ttk.Entry(self.mainframe,
                                      width=10,
                                      style="A.TEntry",
                                      textvariable=self.input_string,
                                      font=("JetBrainsMono Nerd Font Mono", 12))
        self.volume_entry.grid(row=2, column=2)

        for child in self.mainframe.winfo_children():
            # grid_info = child.grid_info()
            # if grid_info["row"] != 0:
            child.grid_configure(padx=5, pady=5)

        self.change_status()
        self.volume_entry.focus()
        root.bind("<Return>", self.change_volume)

    # Seconds to minutes:seconds (uhh hours??)
    def format_duration(self, duration):
        minutes = duration / 60

        if minutes / 60 >= 1:
            hours = minutes // 60
            minutes = minutes % 60
            if minutes < 10:
                minutes = "0" + str(f"{int(minutes)}")
                minutes = str(f"{int(hours)}:{(minutes)}")
            else:
                minutes = str(f"{int(hours)}:{int(minutes)}")
        else:
            minutes = int(minutes)

        seconds = duration % 60
        if seconds < 10:
            seconds = str(f"0{seconds}")
        return (f"{minutes}:{seconds}")

    def get_volume(self):
        sink_string = subprocess.check_output("pactl get-sink-volume 0", shell=True, text=True)
        volume = list(filter(lambda x: "%" in x, sink_string.split(" ")))[0]

        return str(volume)

    # Length and position are returned as seconds

    def get_song_position(self):
        # Get
        # error processing
        try:
            # Will return 0
            position = subprocess.check_output("playerctl position", shell=True, text=True)
            position_num = float(position.strip())
            return int(position_num)
        except subprocess.CalledProcessError as e:
            print(f"Error in getting the song position: {e}")
            return 0

    # Output: seconds
    def get_song_length(self):
        try:
            position = subprocess.check_output("playerctl metadata 'mpris:length'", shell=True, text=True)
            # toi on näköjään millisekunteina
            position_num = float(position.strip()) / 1000000
            return int(position_num)
        except subprocess.CalledProcessError as e:
            print(f"Error in getting song length: {e}")
            return 0

    # Create the widgets that display information about a player
    # Returns their values that can be changed
    def create_player_info(self, row_index):
        self.image = ImageTk.PhotoImage(Image.new("RGB", (128, 128), "blue"))
        self.current_image = Image.new("RGB", (128, 128), "blue")
        self.song_art = ttk.Label(self.playerframe,
                                  image=self.image,
                                  style="A.TLabel")
        self.song_art.grid(row=row_index,
                           column=0,
                           columnspan=2,
                           sticky=(N,S,W,E))

        self.information_string = StringVar()
        self.song_information = ttk.Label(
                self.playerframe,
                style="A.TLabel",
                anchor="c",
                justify="c")
        self.song_information["textvariable"] = self.information_string
        self.song_information.grid(row=row_index,
                                   column=2,
                                   columnspan=2,
                                   sticky=(E, W, S, N))

        # Progressbar updating
        # Get the duration of the song and current place
        # If the current song is playing then keep incrementing this thingy
        self.progress = IntVar(value=self.get_song_position())
        self.progress_str = StringVar(value=self.format_duration(self.progress.get()))
        self.progress_label = ttk.Label(self.playerframe,
                                        style="A.TLabel",
                                        textvariable=self.progress_str)
        self.progress_label.grid(row=row_index+1,
                                 column=0,
                                 sticky=(E, W))


        self.song_progressbar = ttk.Progressbar(self.playerframe,
                                                # the length and units of the song to be different
                                                length=300,
                                                maximum=self.get_song_length(),
                                                mode="determinate",
                                                style="Horizontal.TProgressbar",
                                                orient="horizontal")

        self.song_progressbar["variable"] = self.progress
        self.song_progressbar["mode"] = "determinate"
        self.song_progressbar.grid(row=row_index+1,
                                   column=1,
                                   columnspan=3,
                                   sticky=(W, E))


        self.duration_str = StringVar(value=self.format_duration(self.get_song_length()))
        self.duration_label = ttk.Label(self.playerframe,
                                        style="A.TLabel",
                                        textvariable=self.duration_str)
        self.duration_label.grid(row=row_index+1,
                                 column=4,
                                 sticky=(E, W))
        
        for child in self.playerframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        return (self.song_art, self.information_string, self.progress, self.song_progressbar,
                self.progress_str, self.duration_str)

    # Return a list of album arts, songs, artists and albums or None if there are
    # no players

    def get_data(self):
        # This try catches the case where there are no players and players returns an
        # empty list
        try:
            players = subprocess.check_output("playerctl -l", shell=True, text=True).strip().split()
            metadata_list = list()

            for player in players:
                print(player)
                proxy = self.SESSION_BUS.get("org.mpris.MediaPlayer2." + player,
                                             "/org/mpris/MediaPlayer2")
                metadata = proxy.Get("org.mpris.MediaPlayer2.Player", "Metadata")

                new_image = Image.new("RGB", (128, 128), "gray")

                try:
                    art_response = requests.get(metadata.get("mpris:artUrl"))
                    # Check if the player has a song in the first place
                    # if not then 
                    image_bytes = io.BytesIO(art_response.content)
                    pil_img = Image.open(image_bytes)
                    pil_img = pil_img.resize((128, 128))
                    # new_image = ImageTk.PhotoImage(pil_img)
                    new_image = pil_img
                except Exception as e:
                    print(f"Error in getting art of {player}:\n{e}")

                song = metadata.get("xesam:title")
                artists = ", ".join(metadata.get("xesam:artist"))
                album = metadata.get("xesam:album")

                metadata_list.append((new_image, song, artists, album))

            return metadata_list
        except Exception as e:
            print(f"Error: {e}")
            return None

    def change_status(self):
        playback_data = self.get_data()
        if playback_data is not None and playback_data:

            if not self.playerframe.grid_info():
                self.playerframe.grid(column=0,
                                      row=0,
                                      sticky=(N,W,E,S))
                print("PLAYERFRAME GRIDDED AGAIN")

            row_index = 0

            for player_data in playback_data:

                try:
                    new_song_info = "\n".join(player_data[1:])
                    if self.information_string.get() != new_song_info:
                        player_components = self.create_player_info(row_index)
                        print("PLAYERINFO NOT SAME AND COMPONENTS CREATED")
                    else:
                        player_components = self.create_player_info(row_index)
                except:
                    player_components = self.create_player_info(row_index)

                    print("COMPONENTS CREATED AGAIN")

                # Change this to compare url instead of image
                self.song_image = player_data[0]
                image_diff = ImageChops.difference(self.song_image, self.current_image).getbbox() is not None
                if image_diff:
                    print("IMAGE DRAWN AGAIN")
                    self.current_image = self.song_image
                    self.tk_img = ImageTk.PhotoImage(self.current_image)
                    player_components[0]["image"] = self.tk_img

                # Song info
                player_components[1].set("\n".join(player_data[1:]))

                # Progress & progressbar
                player_components[2].set(self.get_song_position())
                player_components[3]["maximum"] = self.get_song_length()

                # Progress_str
                value = self.format_duration(self.progress.get())
                player_components[4].set(value)

                duration = self.format_duration(self.get_song_length())
                if duration != player_components[5].get() and duration != "0:00":
                    player_components[5].set(duration)
                    print("ZERO")

                row_index = row_index + 2

        else:
            for child in self.playerframe.winfo_children():
                child.grid_forget()
            self.playerframe.grid_forget()

    def poll(self):
        def thread(self):
            thread = Thread(target=self.change_status())
            thread.start()
        # self.change_status()
        thread(self)
        self.volume.set(self.get_volume())
        self.volume_entry.focus()
        root.after(1000, self.poll)

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
            self.change_status()
            self.volume.set(self.get_volume())
            self.input_string.set("")
            self.volume_entry.focus()



root = Tk()
cc = ControlCenter(root)
cc.poll()
root.mainloop()
