import sys

from config.config import Configured
from utils.mqtt import Topic

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error: need config path')

    config = Configured.parse_file(sys.argv[1])
    mqtt = Topic(config=config)
    mqtt.start()
