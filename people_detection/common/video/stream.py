from threading import Thread
from threading import Lock
import cv2


class VideoStream:
    def __init__(self, src, h, w, name="VideoStream"):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        if not self.grabbed:
            raise ValueError(f'failed to fetch input {src}')
        self.init_shape = self.frame.shape[:2]
        self.name = name
        self.stopped = False
        self.lock = Lock()

    def start_stream(self):
        self.vs_thread = Thread(target=self.update, name=self.name, args=())
        self.vs_thread.daemon = True
        self.vs_thread.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.lock.acquire()
            (self.grabbed, self.frame) = self.stream.read()
            self.lock.release()

    def read(self):
        return self.frame

    def ping(self):
        return self.grabbed

    def stop(self):
        self.stopped = True
        self.stream.release()
        self.vs_thread.join()
