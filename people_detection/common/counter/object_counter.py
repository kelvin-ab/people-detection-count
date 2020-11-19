import numpy as np
from json import dumps
from scipy.spatial import distance
from shapely.geometry import Point
from websocket import create_connection
from shapely.geometry.polygon import Polygon


class ObjectCounter:
    def __init__(self, channel, line, area):
        self.known_objects = {}
        self.up_count = 0
        self.down_count = 0
        self.next_id = 0
        self.max_radius = 50
        self.counted_objects = []
        self.channel = channel
        self.start = line[0]
        self.end = line[1]
        self.area = Polygon(area)
        self.direction = 1
        self.socket = create_connection('ws://0.0.0.0:4040/')

    def calc_direction(self, centroid):
        direction = ((centroid[0] - self.start[0]) * (self.end[1] - self.start[1])) - \
                    ((centroid[1] - self.start[1]) * (self.end[0] - self.start[0]))
        return 1 if direction > 0 else -1

    def update(self, detections):
        try:
            centroids = []
            for detection in detections:
                if self.area.contains(Point(detection['centroid'])):
                    centroids.append(detection['centroid'])
                else:
                    pass

            if len(centroids):
                if not self.known_objects:
                    for centroid in centroids:
                        self.known_objects[self.next_id] = dict(centroid=centroid, age=1,
                                                                direction=self.calc_direction(centroid))
                        self.next_id += 1
                else:
                    curr_ids = list(self.known_objects.keys())
                    curr_cents = [object['centroid'] for object in list(self.known_objects.values())]

                    for centroid in centroids:
                        dist = distance.cdist(np.array([centroid]), np.array(curr_cents))
                        if dist.min() < self.max_radius:
                            prev_direction = self.known_objects[curr_ids[np.argmin(dist)]]['direction']
                            curr_direction = self.calc_direction(centroid)

                            if prev_direction != curr_direction and curr_ids[np.argmin(dist)] not in self.counted_objects:
                                if self.direction == 1:
                                    if curr_direction == 1:
                                        self.up_count += 1
                                    else:
                                        self.down_count += 1
                                else:
                                    if curr_direction == -1:
                                        self.down_count += 1
                                    else:
                                        self.up_count += 1

                                self.counted_objects.append(curr_ids[np.argmin(dist)])

                            self.known_objects[curr_ids[np.argmin(dist)]]['centroid'] = centroid
                            self.known_objects[curr_ids[np.argmin(dist)]]['direction'] = curr_direction
                        else:
                            self.known_objects[self.next_id] = dict(centroid=centroid, age=1,
                                                                    direction=self.calc_direction(centroid))
                            self.next_id += 1

                for id, meta in self.known_objects.items():
                    meta['age'] += 1

                for i in list(self.known_objects):
                    if self.known_objects[i]['age'] > 75 or not self.area.contains(Point(self.known_objects[i]['centroid'])): #or centroid exits the box
                        del self.known_objects[i]

            else:
                # reset
                self.next_id = 0
                self.counted_objects = []

            self.socket.send(dumps({
                'event': 'count',
                'data': {
                    'channel': self.channel,
                    'up': self.up_count,
                    'down': self.down_count
                }
            }))
            print('channel: ', self.channel, ' up: ', self.up_count, ' down: ', self.down_count)
        except Exception as e:
            print(str(e))
