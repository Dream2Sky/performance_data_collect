import configparser

from utils import singleton


class Config(object):
    def __init__(self, conf_path):
        self._config = configparser.RawConfigParser()
        self._config.read(conf_path)

    def get_config(self, _section, _key=None, conf_type=bytes, default=None):
        try:
            if _key is None:
               return self._config.items(_section)
            else: 
                if bool == conf_type or conf_type == bool:
                    return self._config.getboolean(_section, _key)
                elif int == conf_type:
                    return int(self._config.get(_section, _key))
                else:
                    return self._config.get(_section, _key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

@singleton
class Environment(object):
    
    mongo_config_path = "db.conf"
    def __init__(self):
        self.mongo_config = Config(self.mongo_config_path)


environment = Environment()