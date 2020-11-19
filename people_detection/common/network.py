import cv2
import config
import numpy as np
from queue import Queue
from os.path import join
from os.path import isdir
from os.path import splitext
from openvino.inference_engine import IECore
from common.utils.network import get_blob_shape


class Network:
    def __init__(self, model, device='CPU', batch_size=1, num_requests=2, dyn_batch=False):

        if not isdir(join(config.MODEL_DIR, model)):
            raise FileNotFoundError(f'model {model} does not exist')

        self.batch_size = batch_size
        self.dynamic_batch = dyn_batch
        model_xml = join(config.MODEL_DIR, model, model + '.xml')
        model_bin = splitext(model_xml)[0] + ".bin"
        ie_core = IECore()
        net = ie_core.read_network(model=model_xml, weights=model_bin)
        new_shapes = {}
        for input_layer_name, input_layer in net.inputs.items():
            new_shapes[input_layer_name] = get_blob_shape(input_layer, batch_size)
        if new_shapes:
            net.reshape(new_shapes)

        if self.dynamic_batch:
            self.model = ie_core.load_network(network=net, device_name=device, num_requests=num_requests,
                                              config={"DYN_BATCH_ENABLED": "YES", 'CPU_THREADS_NUM': str(6)})
        else:
            self.model = ie_core.load_network(network=net, device_name=device, num_requests=num_requests,
                                              config={'CPU_THREADS_NUM': str(28),
                                                      'CPU_THROUGHPUT_STREAMS': str(28)})

        self.input_blob = next(iter(self.model.inputs))
        self.output_blob = next(iter(self.model.outputs))
        self.input_height, self.input_width = self.model.inputs[self.input_blob].shape[2:]
        self.avail_reqs = Queue(num_requests)
        for ireq in range(num_requests):
            self.avail_reqs.put(ireq)
        self.busy_reqs = Queue(num_requests)
        self.busy_batch_reqs = Queue(num_requests)

    def preprocess(self, batch):
        resized = [cv2.resize(image, (self.input_width, self.input_height)).transpose((2, 0, 1)) for image in batch]
        return resized, batch

    def predict(self, input, input_x, serial=None):
        avail_req = self.avail_reqs.get_nowait()
        # avail_req = self.model.get_idle_request_id()
        # if avail_req < 0:
        #     status = self.model.wait(num_requests=1)
        #     if status != 0:
        #         raise Exception("Wait for idle request failed!")
        #     avail_req = self.model.get_idle_request_id()
        #     if avail_req < 0:
        #         raise Exception("Invalid request id!")
        tensor = np.stack(input)
        if self.dynamic_batch:
            self.model.requests[avail_req].set_batch(len(input))
            placeholder = np.zeros((self.batch_size, 3, self.input_height, self.input_width))
            placeholder[:tensor.shape[0], :tensor.shape[1], :tensor.shape[2], :tensor.shape[3]] = tensor
            self.model.requests[avail_req].async_infer({self.input_blob: placeholder})
        else:
            self.model.requests[avail_req].async_infer({self.input_blob: tensor})
        self.model.requests[avail_req].wait(0)
        # self.model.requests[avail_req].wait()
        self.busy_batch_reqs.put([input_x, avail_req, serial])
        self.busy_reqs.put_nowait(avail_req)

