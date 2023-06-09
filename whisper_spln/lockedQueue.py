from threading import Lock
from time import time
import os

class lockedQueue():
    
    def __init__(self):
        self.lock = Lock()
        self.queue = []
        self.isRunning = False
        self.actualTime = 0
        self.actualSize = 0
        self.meanTime = 0
        self.numConversions = 0
        self.loadTime()
    
    def loadTime(self):
        with open('whisper_spln/conf/exec_time', 'r') as file:
            lines = [line.rstrip() for line in file]
        
        if len(lines) == 2:
            self.meanTime = float(lines[0])
            self.numConversions = float(lines[1])
    
    def saveTime(self):
        self.lock.acquire()
        
        with open('whisper_spln/conf/exec_time', 'w') as file:
            file.write(f"{self.meanTime}\n")
            file.write(f"{self.numConversions}\n")
            
        self.lock.release()

    def put(self, item):
        self.lock.acquire()
        self.queue.append((item, os.stat(item).st_size))
        prediction = self.getTimePrediction()
        self.lock.release()
        
        return prediction
    
    def get(self):
        self.lock.acquire()
        self.actualSize = self.queue[0][1]
        self.actualTime = time()
        self.isRunning = True
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
    
    def calculteNewMean(self):
        self.lock.acquire()
        
        meanTime= (time() - self.actualTime) / self.actualSize
        
        self.meanTime = (self.meanTime * self.numConversions + meanTime) / (self.numConversions + 1)
        self.numConversions += 1
        self.isConverting = False
        
        self.lock.release()
        
    def stopRunning(self):
        self.lock.acquire()
        self.isRunning = False
        self.lock.release()
        
    def getTimePrediction(self):
        prediction = 0
        for item in self.queue:
            prediction += item[1] * self.meanTime
        
        if self.isRunning:
            timeDifference = self.actualSize * self.meanTime - (time() - self.actualTime)
            if timeDifference > 0:
                prediction += timeDifference
        
        return prediction
