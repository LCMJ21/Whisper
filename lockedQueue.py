from threading import Lock

class lockedQueue():
    
    def __init__(self):
        self.lock = Lock()
        self.queue = []

    def put(self, item):
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
    
    def get(self):
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        return item
    
    def empty(self):
        self.lock.acquire()
        empty = len(self.queue) == 0
        self.lock.release()
        return empty
    
    def all_items(self):
        self.lock.acquire()
        items = self.queue.copy()
        self.lock.release()
        return items