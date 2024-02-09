import tkinter as tk
from tkinter import messagebox
import json
import socket
import threading
import os

# Client

HOST = "127.0.0.1"
SERVER = "localhost"
SND_PORT = 12345
REC_PORT = 12346

app = tk.Tk()

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

def open_popup(data):
   top= tk.Toplevel(app)
   top.geometry("750x250")
   top.title("Child Window")
   tk.Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)

def main():
    app.title("SyncSax")
    #if os.name == "nt":
    #    app.state("zoomed")
    #else:
    #    app.attributes("-zoomed", True)

    
    options = list(videos.keys())

    selected = tk.StringVar()
    selected.set(options[0])

    drop = tk.OptionMenu(app, selected, *options)
    drop.pack()
    btn = tk.Button(app, text = "Start", command = lambda: call(selected))
    btn.pack()
  
    label = tk.Label(app, text = " ")
    label.pack() 

    listener_thread = threading.Thread(target=recv, daemon=True)
    listener_thread.start()

    app.mainloop()
    print("test")

if __name__ == "__main__":
    register()
    main()

