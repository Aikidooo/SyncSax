from datetime import datetime
import json
import socket

# Server

HOST = "localhost"  # Standard loopback interface address (localhost)
REC_PORT = 12345
SND_PORT = 12346

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, REC_PORT))
sock.listen()

recipients = set()


def shoutout(call):
    """Distribute a call to all known recipients after adding a timestamp"""
    print(f"Performing shoutout to {recipients}")
    pack = {
        "initiator": call["initiator"],
        "video": call["video"],
        "timestamp": str(datetime.now().time())
    }
    for recipient in recipients:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
            print(recipient)
            send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            send_sock.connect((recipient, SND_PORT))
            send_sock.sendall(json.dumps(pack).encode())


def recv():
    """Wait for incoming calls or register packets"""
    print("Waiting for connection...")

    conn, addr = sock.accept()

    print(f"Received transmission from {addr[0]}")

    try:
        data = conn.recv(1024)
        msg = data.decode("utf-8")
    except socket.error:
        return
    finally:
        conn.close()

    if msg == "register":
        global recipients
        recipients.add(addr[0])
        print(f"Added recipient '{addr[0]}'")
        return

    return json.loads(msg)

def main():

    while True:
        data = recv()
        if not data:
            continue
        print(data)
        shoutout(data)

if __name__ == "__main__":
    try:
        main()
    finally:
        sock.close()


# Packet: video, timestamp, initiator
