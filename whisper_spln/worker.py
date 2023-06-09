from threading import Event, Thread
from time import sleep
import whisper

from whisper_spln.lockedQueue import lockedQueue


class Worker(Thread):

    def __init__(self, shared_queue: lockedQueue, event_shutdown: Event):
        Thread.__init__(self)
        self.shared_queue = shared_queue
        self.event_shutdown = event_shutdown
        self.shutdown = False
        self.model = whisper.load_model("base")

    def run(self):
        print("Worker started")
        while not self.shutdown:
            self.process_queue()
            sleep(20)  # Sleep for 20 seconds to wait for more work
        self.shared_queue.saveTime()
        self.event_shutdown.set()
        print("Worker stopped")

    def process_queue(self):
        self.shutdown = True if self.shared_queue.empty() else False

        while not self.shared_queue.empty():
            file = self.shared_queue.get()
            print("Handling ------>", file[0])
            try:
                result = self.model.transcribe(file[0], fp16=False)["text"]
                self.shared_queue.calculteNewMean()
            except Exception as e:
                result = f"Error: {e}"
                self.shared_queue.stopRunning()
                
            open("result.txt", "a").write(
                f"{file[0]}\n{result}\n-------------\n")
            print("Finished ------>", file[0])
