import tkinter as tk
import json
import socket
import os

HOST = socket.gethostname()
SERVER = "google.com"
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

with open("videos.json") as f:
    videos: dict = json.load(f)

def register():
    """Register to the Server at startup for the day"""
    pass

def call(video: tk.StringVar):
    """Send a call to the Server, containing desired video and initiator"""
    video = video.get()
    pack = {
        "initiator": socket.gethostname(),
        "video": videos[video]
    }
    sock.connect((SERVER, PORT))
    sock.sendall(json.dumps(pack).encode())

def recv():
    """Wait for incoming instructions by the Server"""
    pass


def main():
    app = tk.Tk()
    app.title("SyncSax")
    if os.name == "nt":
        app.state("zoomed")
    else:
        app.attributes("-zoomed", True)

    
    options = list(videos.keys())

    selected = tk.StringVar()
    selected.set(options[0])

    drop = tk.OptionMenu(app, selected, *options)
    drop.pack()
    btn = tk.Button(app, text = "Start", command = lambda: call(selected))
    btn.pack()
  
    label = tk.Label(app, text = " ")
    label.pack() 

    app.mainloop()

if __name__ == "__main__":
    register()
    main()

