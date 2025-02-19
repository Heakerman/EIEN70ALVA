import threading
import time

class Monitor:
    def __init__(self):
        self.lock = threading.Lock()