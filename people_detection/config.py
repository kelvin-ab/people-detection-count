MODEL_DIR = 'models'
MODEL_BLOB_INFO = {
    'age-gender-recognition-retail-0013': {
        'gender': ['female', 'male'],
        'emotion': ['neutral', 'happy', 'sad', 'surprise', 'anger']
    },
    'vehicle-attributes-recognition-barrier-0039': {
        'color': ['white', 'gray', 'yellow', 'red', 'green', 'blue', 'black'],
        'type': ['car', 'bus', 'truck', 'van']
    }
}

MQTT_CREDS = {
    'host': 'localhost',
    'port': 1883,
    'keep_alive': 60
}

MQTT_GLOBAL_URI = 'global'

MQTT_TOPICS = {
    # 'person-detection-retail-0013': 'person-detection-retail-0013',
    # 'person-vehicle-bike-detection-crossroad-0078': 'person-vehicle-bike-detection-crossroad-0078',
    'face-detection-retail-0005': 'face-detection-retail-0005.json',
    # 'face-detection-retail-0004': 'face-detection-retail-0004',
    # 'face-detection-adas-0001': 'face-detection-adas-0001',
    # 'vehicle-detection-adas-0002': 'vehicle-detection-adas-0002',
    'counter': 'counter/',
    'stream': 'stream'
}

SERVER_DB = {
    'config_fetch': 'http://0.0.0.0:2255/config/fetch'
}