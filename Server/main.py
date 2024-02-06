from datetime import datetime
import json
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

recipients = []


def main():

    while True:
        data = recv()
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
    data, addr = sock.recvfrom(1024)

    print(f"Received data from {addr}")

    msg = data.decode("utf-8")

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
