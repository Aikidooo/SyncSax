import tkinter as tk
from tkinter import messagebox

import json
import socket
import threading
from pathlib import Path
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip

# Client

HOST = "127.0.0.1"
SERVER = "localhost"
SND_PORT = 12345
REC_PORT = 12346

VID_DIR = Path.home() / "videos" / "SyncSax"
VID_LENGTH = 600

root = tk.Tk()

with open("videos.json") as f:
    videos: dict = json.load(f)

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((SERVER, SND_PORT))
    return sock

def register():
    """Register to the Server at startup for the day"""
    with connect() as sock:
        sock.sendall(b"register")

def call(video: tk.StringVar):
    """Send a call to the Server, containing desired video and initiator"""

    video = video.get()
    print(f"Sending call with video '{video}'")

    pack = {
        "initiator": socket.gethostname(),
        "video": videos[video]
    }
    with connect() as sock:
        sock.sendall(json.dumps(pack).encode())

def recv():
    """Wait for incoming instructions by the Server"""
    print("Ready to receive shoutouts")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, REC_PORT))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        open_popup(json.loads(data.decode()))
        conn.close()

def vid_file_exists(name) -> bool:
    if not os.path.isdir(VID_DIR):
        os.mkdir(VID_DIR)
        return False
    return os.path.exists(VID_DIR / f"{name}.mp4")

def download_vid(id: str):
    print(f"Downloading video {id}")
    tmp_file = YouTube(f"https://www.youtube.com/watch?v={id}").streams.get_highest_resolution().download()
    video = VideoFileClip(tmp_file).subclip(0, VID_LENGTH)
    video.write_videofile(VID_DIR / f"{id}.mp4")
    os.remove(tmp_file)
    print("Done")

def open_popup(data):

    res = messagebox.askquestion("Aufruf erhalten", f"{data['initiator']} möchte folgendes Video starten: {data['video']} \nMöchtest du beitreten?")
    if res == "yes":
        print("Accepted call")
        if vid_file_exists(data["video"]):
            print("Using local videofile")
        else:
            download_vid(data["video"])
    else:
       print("no")

def main():
    root.title("SyncSax")
    #if os.name == "nt":
    #    app.state("zoomed")
    #else:
    #    app.attributes("-zoomed", True)

    
    options = list(videos.keys())

    selected = tk.StringVar()
    selected.set(options[0])

    drop = tk.OptionMenu(root, selected, *options)
    drop.pack()
    btn = tk.Button(root, text = "Start", command = lambda: call(selected))
    btn.pack()
  
    label = tk.Label(root, text = " ")
    label.pack() 

    frame = tk.Frame(root)
    frame.pack()

    listener_thread = threading.Thread(target=recv, daemon=True)
    listener_thread.start()

    
    root.mainloop()
    print("test")

if __name__ == "__main__":
    register()
    main()

