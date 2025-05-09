import json
import logging
import os

logger = logging.getLogger()

class RobotConfig:

    def __init__(self):
        if os.getenv('DOCKER', 'false').lower() == 'true':
            self.CONFIG_NAME = "robot_config.json"
            self.CONFIG_PATH = os.path.join('/', 'config', self.CONFIG_NAME)
        else:
            self.CONFIG_NAME = "robot_local_config.json"
            self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), self.CONFIG_NAME)
        self.__load_config()

    def __save_config(self):
        with open(self.CONFIG_PATH, 'w') as f:
            json.dump(self.__config, f)

    def __load_config(self):
        try:
            with open(self.CONFIG_PATH, 'r') as f:
                self.__config = json.load(f)
        except FileNotFoundError:
            logger.error('Config file not found')
            self.__config = {}
            self.__config['host'] = '0.0.0.0'               # Default host
            self.__config['port'] = 48569                   # Default port
            self.__config['timeout'] = 5                    # Default timeout
            self.__config['max_tcp_attempts'] = 5           # Default max TCP attempts
            self.__config['ping_interval'] = 15            # Default check interval
            self.__save_config()
    
    def __getitem__(self, key):
        return self.__config[key]
    
    def __setitem__(self, key, value):
        self.__config[key] = value
        self.__save_config()

if __name__ == '__main__':
    config = RobotConfig()
    print(config['host'])
    print(config['port'])
    print(config['timeout'])
    print(config['connection_timeout'])
    print(config['max_connection_attempts'])
    print(config['max_tcp_attempts'])
    config['host'] = '0.0.0.0'
    config['port'] = 48569
