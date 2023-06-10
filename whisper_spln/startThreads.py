
from threading import Event
from whisper_spln.worker import Worker
from whisper_spln.lockedQueue import lockedQueue
from whisper_spln.listener import Listener
import sys


def start_threads():
    print(sys.argv)
    dict = {
        "filename": sys.argv[1],
        "outputLang": None,
    }
    event_shutdown = Event()
    shared_queue = lockedQueue()
    prediction = shared_queue.put(dict)
    listener = Listener(shared_queue, event_shutdown)
    worker = Worker(shared_queue, event_shutdown)
    print(
        f'Received: Your file will be ready in {round(prediction, 2)} seconds!')
    listener.start()
    worker.start()


start_threads()
