import socket
import json
import threading
import struct
import time
from packet import CallPack

multicast_group = "ff02::1"
multicast_port = 12345



def send_call():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("::", multicast_port)) 

    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)

    call_pack = json.dumps(CallPack("xy").pack())

    sock.sendto(call_pack.encode("utf-8"), (multicast_group, multicast_port))
    sock.close()

def recv_call():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("::", multicast_port)) 

    addrinfo = socket.getaddrinfo(multicast_group, None)[0]
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])

    mreq = group_bin + struct.pack('@I', 0)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    try:
        while True:
            raw_data, addr = sock.recvfrom(1024)
            data = json.loads(raw_data.decode("utf-8"))
            print("Received Packet: ", data)
            sock.close()
            return
    except Exception as e:
        print(e)
        sock.close()

if __name__ == "__main__":
    receiver = threading.Thread(target=recv_call)
    receiver.start()
    send_call()
    time.sleep(1)
    receiver.join()