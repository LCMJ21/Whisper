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

    def put(self, item):
        self.lock.acquire()
        item["size"] = os.stat(item["filename"]).st_size
        self.queue.append(item)
        prediction = self.getTimePrediction()
        self.lock.release()

        return prediction

    def get(self):
        self.lock.acquire()
        self.actualSize = self.queue[0]["size"]
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

        meanTime = (time() - self.actualTime) / self.actualSize

        self.meanTime = (self.meanTime * self.numConversions +
                         meanTime) / (self.numConversions + 1)
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
            prediction += item["size"] * self.meanTime

        if self.isRunning:
            timeDifference = self.actualSize * \
                self.meanTime - (time() - self.actualTime)
            if timeDifference > 0:
                prediction += timeDifference

        return prediction
