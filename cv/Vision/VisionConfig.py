import json
import logging
import os

logger = logging.getLogger()

class VisionConfig:

    def __init__(self):
        if os.getenv('DOCKER', 'false').lower() == 'true':
            self.CONFIG_NAME = "vision_config.json"
            self.CONFIG_PATH = os.path.join('/', 'config', self.CONFIG_NAME)
        else:
            self.CONFIG_NAME = "vision_local_config.json"
            self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), self.CONFIG_NAME)
        self.__load_config()

    def __save_config(self):
        #logger.debug("Save config init@")
        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.__config, f, ensure_ascii=False, indent=4)
        #logger.debug("Save config ok")
    def __load_config(self):
        try:
            logger.info('Loading config for vision class')
            with open(self.CONFIG_PATH, 'r') as f:
                self.__config = json.load(f)
        except FileNotFoundError:
            logger.error('Config file not found')
            self.__config = {}
            self.__config['display_box'] = True
            self.__config['display_pose'] = True
            self.__config['display_coordinates'] = True
            self.__config['display_confidence'] = True
            self.__config['display_fps'] = True
            self.__config['class_names'] = ["Empty"]
            self.__config['models'] = {"Empty": "empty.pt"}    
            self.__config['minimal_confidences'] =  {"Empty": 1}
            self.__config['model_type'] = {"Empty": "detect"}
            self.__save_config()
    
    def __getitem__(self, key):
        #logger.debug(f'Get item: key={key}, value={self.__config[key]}')
        return self.__config[key]
    
    def __setitem__(self, key, value):
        #logger.debug(f'Set item: key={key}, value={self.__config[key]}')
        self.__config[key] = value
        self.__save_config()

if __name__ == '__main__':
    config = VisionConfig()
    print(config['models'])


