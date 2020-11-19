from threading import Thread
from threading import Lock
from common.video import stream


class Streamer:
    def __init__(self, channels, h, w):
        self.channels = channels
        self.streams = []

        for channel in self.channels:
            vs = stream.VideoStream(channel, h, w).start_stream()
            if vs.ping():
                self.streams.append(vs)
            else:
                raise ValueError(f"Can't connect to {channel}")
        self.batch = []
        self.s_mutex = Lock()

    def start_streamer(self):
        self.s_thread = Thread(target=self.next, args=())
        self.s_thread.daemon = True
        self.s_thread.start()

    def next(self):
        while True:
            batch = []
            for streamx in self.streams:
                batch.append(streamx.read())
            # self.s_mutex.acquire()
            self.batch = batch
            # self.s_mutex.release()
