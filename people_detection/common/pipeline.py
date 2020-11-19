import config
from threading import Thread
from common.network import Network
from common.streamer import Streamer
from common.video.render import Render


class Pipeline(Network, Streamer, Render):
    def __init__(self, model, channels, batch_size, num_requests, detection_threshold=0.75, output_size=5, counter=False):

        Network.__init__(self, model, batch_size=batch_size, num_requests=num_requests)
        h, w = self.input_height, self.input_width
        Streamer.__init__(self, channels, h, w)
        Render.__init__(self, model=model, batch_size=batch_size, queue_size=output_size)
        Streamer.start_streamer(self)
        Render.start_render(self)
        self.detection_threshold = float(detection_threshold)
        self.counter = counter

    def start_pipe(self):
        self.p_thread1 = Thread(target=self.infer, args=())
        self.p_thread1.daemon = True
        self.p_thread1.start()

        self.p_thread2 = Thread(target=self.render, args=())
        self.p_thread2.daemon = True
        self.p_thread2.start()

        self.p_thread1.join()
        self.p_thread2.join()

    def infer(self):
        while True:
            if not self.batch:
                continue
            preprocessed, untouched = self.preprocess(self.batch)
            try:
                self.predict(preprocessed, untouched)
            except Exception as e:
                continue

    def render(self):
        while True:
            try:
                completed = self.busy_batch_reqs.get_nowait()
            except Exception as e:
                # print('no busy id')
                continue
            if self.model.requests[completed[1]].wait(-1) == 0:
                # print('***************************************************')
                self.avail_reqs.put(completed[1])
                output = self.model.requests[completed[1]].outputs
                filtered_detections = output[self.output_blob] \
                    [(output[self.output_blob][:, :, :, 2] > self.detection_threshold)]
                results = self.postprocess(filtered_detections, self.streams, self.channels)
                try:
                    # self.avail_reqs.put(completed[1])
                    if True:
                        self.output.put_nowait(results)
                        self.draw(completed[0], filtered_detections, self.streams)
                        if self.counter:
                            self.mqtt_client.publish("topic/" + config.MQTT_TOPICS['counter'] + self.model_name, str(results))
                            print("Send to counter")
                except Exception as e:
                    print(str(e))
