from socket import gethostname
from datetime import datetime

class CallPack:
    def __init__(self, video: str):
        self.video: str = video
    
    def pack(self):
        data = {
            "video": self.video,
            "initiator": gethostname(),
            "timestamp": str(datetime.now().time())
        }