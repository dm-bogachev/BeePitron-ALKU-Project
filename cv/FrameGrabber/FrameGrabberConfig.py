import json
import logging
import os

logger = logging.getLogger()

class FrameGrabberConfig:

    def __init__(self):
        if os.getenv('DOCKER', 'false').lower() == 'true':
            self.CONFIG_NAME = "camera_config.json"
            self.CONFIG_PATH = os.path.join('/', 'app', 'config', self.CONFIG_NAME)
        else:
            self.CONFIG_NAME = "camera_local_config.json"
            self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), self.CONFIG_NAME)
        self.__load_config()

    def __save_config(self):
        with open(self.CONFIG_PATH, 'w') as f:
            json.dump(self.__config, f)

    def __load_config(self):
        logger.info('Loading config for frame grabber class')
        try:
            with open(self.CONFIG_PATH, 'r') as f:
                self.__config = json.load(f)
        except FileNotFoundError:
            logger.error('Config file not found')
            self.__config = {}
            self.__config['exposure'] = 10000
            self.__config['markers_x_distance'] = 4100
            self.__config['markers_y_distance'] = 2860
            self.__config['camera_type'] = 'hik'
            self.__config['webcamera_address'] = 0
            self.__config["display_width"] = 1920
            self.__config["display_height"] = 1080
            self.__save_config()
    
    def __getitem__(self, key):
        return self.__config[key]
    
    def __setitem__(self, key, value):
        self.__config[key] = value
        self.__save_config()

if __name__ == '__main__':
    config = FrameGrabberConfig()
    print(config['exposure'])


