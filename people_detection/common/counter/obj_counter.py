import config
import argparse
from ast import literal_eval
import paho.mqtt.client as mqtt
from collections import defaultdict
from object_counter import ObjectCounter


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/" + config.mqtt_topic + args.model)


def on_message(client, userdata, msg):
    raw_info = eval(msg.payload.decode())
    result = defaultdict(list)

    for object in raw_info:
        result[object['channel']].append(object)
    result_list = list(result.values())

    for channel_list in result_list:
        if channel_list[-1]['channel'] in counters.keys():
            counters[channel_list[-1]['channel']].update(channel_list)


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='List the content of a folder')
    my_parser.add_argument('-m', '--model', help='name of the model', required=True, type=str)
    my_parser.add_argument('-r', '--regions', help='count regions', required=True, type=str)
    args = my_parser.parse_args()

    counters = {}
    for channel, region_meta in literal_eval(args.regions).items():
        counter = ObjectCounter(channel, region_meta['line'], region_meta['area'])
        counters[channel] = counter

    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
