from datetime import datetime
import json
import socket

HOST = ""  # Standard loopback interface address (localhost)
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

recipients = []


def main():

    while True:
        data = recv()
        print(recipients)
        if not data:
            continue
        shoutout(data)


def shoutout(call):
    """Distribute a call to all known recipients after adding a timestamp"""
    pack = {
        "initiator": call["initiator"],
        "video": call["video"],
        "timestamp": str(datetime.now().time())
    }

    for recipient in recipients:
        sock.sendto(json.dumps(pack).encode(), (recipient, PORT))


def recv():
    conn, addr = sock.accept()

    print(f"Received data from {addr}")

    try:
        data = conn.recv(1024)
        msg = data.decode("utf-8")
    except socket.error:
        return
    finally:
        conn.close()

    if msg == "register":
        global recipients
        recipients.append(addr)
        return

    return json.loads(msg)


if __name__ == "__main__":
    try:
        main()
    finally:
        sock.close()


# Packet: video, timestamp, initiator
