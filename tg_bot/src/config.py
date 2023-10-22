import logging
import os
from collections import defaultdict
from typing import Any, List, Optional

import yaml

from src.devices.light import Light

logger = logging.getLogger()
logging.getLogger("peewee").setLevel(
    logging.INFO
)  # Prevent debug messages from peewee lib


class ConfigError(RuntimeError):
    def __init__(self, msg: str):
        super(ConfigError, self).__init__("%s" % (msg,))


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            func(*args, **kwargs)
            wrapper.has_run = True

    wrapper.has_run = False
    return wrapper


# import pymorphy2
# morph = pymorphy2.MorphAnalyzer()
#
# with open('barmaglot.txt',  encoding='utf-8') as f:
#     ls = []
#     for line in f:
#         lst = line.split()
#
#         words = []
#         for word in lst:
#             p = morph.parse(word)[0]  # делаем разбор
#             words.append(p.normal_form)
#
#         ls.append(words)


class Config:
    """Creates a Config object from a YAML-encoded config file from a given filepath"""

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance

        cls._instance = super(Config, cls).__new__(cls)
        cls._instance.__init__(*args, **kwargs)

        return cls._instance

    @run_once
    def __init__(self, filepath: str = "config.yaml"):
        self.filepath = filepath
        if not os.path.isfile(filepath):
            raise ConfigError(f"Config file '{filepath}' does not exist")

        # Load in the config file at the given filepath
        with open(filepath) as file_stream:
            self.config_dict = yaml.safe_load(file_stream.read())

        # Parse and validate config options
        self.devices = defaultdict(list)
        self._parse_config_values()

    def _parse_config_values(self):
        """Read and validate each config option"""
        self._parse_lights(self._get_cfg(["services", "light"], required=False))
        self.token = self._get_cfg(["config", "token"])

        self.voice_files_directory = self._get_cfg(
            ["config", "voice_files_directory"], default="/voice_messages"
        )
        if not os.path.exists(self.voice_files_directory):
            os.makedirs(self.voice_files_directory)
        self.host = self._get_cfg(["config", "host"], default="0.0.0.0")
        self.port = self._get_cfg(["config", "port"], default=8002)
        self.language = self._get_cfg(["config", "language"], default="ru-RU")

    def _get_cfg(
        self,
        path: List[str],
        default: Optional[Any] = None,
        required: Optional[bool] = True,
    ) -> Any:
        """Get a config option from a path and option name, specifying whether it is
        required.

        Raises:
            ConfigError: If required is True and the object is not found (and there is
                no default value provided), a ConfigError will be raised.
        """
        # Sift through the the config until we reach our option
        config = self.config_dict
        for name in path:
            config = config.get(name)

            # If at any point we don't get our expected option...
            if config is None:
                # Raise an error if it was required
                if required and not default:
                    raise ConfigError(f"Config option {'.'.join(path)} is required")

                # or return the default value
                return default

        # We found the option. Return it.
        return config

    def _parse_lights(self, lights_list):
        for light in lights_list:
            name = light["name"]
            # print(name)
            # name = name.encode('cp1251')
            # print(name)
            # name = name.decode('utf8')
            # print(name)
            endpoint_on = light["endpoint_on"]
            endpoint_off = light["endpoint_off"]
            light_device = Light(name, endpoint_on, endpoint_off)
            self.devices["lights"].append(light_device)
