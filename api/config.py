#! /usr/bin/python

import ConfigParser
import os


class Config():
    """ Reads the plugin config, formats values where needed, and returns
    config as dict of dicts
    """

    # Define Config Defaults for MFD Plugin components
    DEFAULTS = {
        "multifile-downloader": {
            "file-name": "download",
            "file-extension": "tar.gz",
            "tmp-location": "/tmp",
            "serve-location": "/export/downloads",
            "serve-directory": "/downloads"
        },
        "zmq-client": {
            "socket-url": "tcp://localhost",
            "socket-port": "5555"
        }, 
        "zmq-server": {
            "socket-url": "tcp://*",
            "socket-port": "5555"
        }
    }

    _config = None
    # def __init__(self):
    #     self._config = None
        
    
    def get_config(self):
        if self._config is None:

            # Read config file
            dir_path = os.path.dirname(os.path.realpath(__file__))
            config_filepath = os.path.join(dir_path, "config.ini")

            cfg = ConfigParser.ConfigParser()
            cfg.read(config_filepath)

            sections = cfg.sections()

            # Insert default values where not provided by config.ini
            for section in sections:
                for (key, value) in cfg.items(section):
                    # Empty values are an empty string ("")
                    if value == "":
                        cfg.set(section, key, self.DEFAULTS[section][key])

            self._config = cfg

        return self._config
    

# # For testing only:
# if __name__ == "__main__":
#     config = Config()
#     config = config.get_config()
