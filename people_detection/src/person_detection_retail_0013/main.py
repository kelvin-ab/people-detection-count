import configparser
from sys import executable
from subprocess import Popen
from common.pipeline import Pipeline


class PersonRetail(Pipeline):
    def __init__(self, model, channels, batch_size, num_requests, detection_threshold, output_size, counter):
        super().__init__(model, channels, batch_size, num_requests, detection_threshold, output_size, counter)


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('src/person_detection_retail_0013/config.ini')
    model_name = config['MODELS']['NAME']
    max_batch_size = int(config['INFERENCE']['MAX_BATCH_SIZE'])
    num_requests = int(config['INFERENCE']['NUM_REQUESTS'])
    detection_threshold = float(config['INFERENCE']['DETECTION_THRESHOLD'])
    output_size = int(config['OUTPUT']['QUEUE_SIZE'])
    FILES = eval(config['MEDIA']['FILES'])
    channels, regions = [], {}
    for _file, _line, _area in FILES:
        regions[_file] = dict(line=_line, area=_area)
        channels.append(_file)

    assert len(channels) <= max_batch_size, "[SC AssertionError] batch size mis-match"

    if regions:
        Popen([executable, "src/person_detection_retail_0013/common/counter/obj_counter.py", "-m", model_name, "-r",
               str(regions)])

    person = PersonRetail(model=model_name,
                          channels=channels,
                          batch_size=len(channels),
                          num_requests=num_requests,
                          detection_threshold=detection_threshold,
                          output_size=output_size,
                          counter=True if regions else False)
    person.start_pipe()
