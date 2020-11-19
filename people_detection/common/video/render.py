import cv2
import config
from time import time
from json import dumps
from queue import Queue
from base64 import b64encode
from threading import Thread
import paho.mqtt.client as mqtt
from imutils import build_montages
from websocket import create_connection


class Render:
    def __init__(self, model, batch_size, queue_size=15):
        self.model_name = model
        self.batch_size = batch_size
        self.output = Queue(queue_size)
        self.display = Queue(queue_size)
        self.montage_dim = (1, 1)
        if self.batch_size > 2:
            if self.batch_size % 2 == 0:
                self.montage_dim = (self.batch_size // 2, self.batch_size // 2)
            else:
                self.montage_dim = ((self.batch_size + 1) // 2, (self.batch_size + 1) // 2)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(config.MQTT_CREDS['host'], config.MQTT_CREDS['port'],
                                 config.MQTT_CREDS['keep_alive'])
        self.socket = create_connection('ws://0.0.0.0:4040/')

    def start_render(self):
        self.r_thread = Thread(target=self.publish_to_mqtt, args=())
        self.r_thread.daemon = True
        self.r_thread.start()

        self.d_thread = Thread(target=self.show_montage, args=())
        self.d_thread.daemon = True
        self.d_thread.start()

    def postprocess(self, detections, streams, channels):
        raw = []
        for detection in detections:
            xmin = abs(int(detection[3] * streams[int(detection[0])].init_shape[1]))
            ymin = abs(int(detection[4] * streams[int(detection[0])].init_shape[0]))
            xmax = abs(int(detection[5] * streams[int(detection[0])].init_shape[1]))
            ymax = abs(int(detection[6] * streams[int(detection[0])].init_shape[0]))
            centroid = (xmin + xmax) / 2, (ymin + ymax) / 2
            timestamp = time()
            channel = channels[int(detection[0])]
            raw.append({
                'channel': channel,
                'timestamp': timestamp,
                'bbox': [xmin, ymin, xmax, ymax],
                'centroid': centroid,
                'class': detection[1],
                'model': self.model_name
            })
        return raw

    def draw(self, images, detections, streams):
        for detection in detections:
            xmin = abs(int(detection[3] * streams[int(detection[0])].init_shape[1]))
            ymin = abs(int(detection[4] * streams[int(detection[0])].init_shape[0]))
            xmax = abs(int(detection[5] * streams[int(detection[0])].init_shape[1]))
            ymax = abs(int(detection[6] * streams[int(detection[0])].init_shape[0]))
            cv2.rectangle(images[int(detection[0])], (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.line(images[int(detection[0])], (658, 474), (1558, 536), (0, 255, 0), 2)

        self.display.put_nowait(images)

    def publish_to_mqtt(self):
        while True:
            try:
                object = self.output.get_nowait()
            except Exception:
                continue

    def show_montage(self):
        while True:
            try:
                images = self.display.get_nowait()
            except Exception:
                continue
            montage = build_montages(images, (640, 480), self.montage_dim)
            for m in montage:
                flag, buffer = cv2.imencode(".png", m)
                # cv2.imshow('window', m)
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break
                if not flag:
                    continue
                # b64_img = b64encode(buffer).decode('ascii')
                # self.socket.send(dumps({"event": "image", "data": b64_img}))
                print('published')