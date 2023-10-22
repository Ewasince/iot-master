import logging

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.light import (PLATFORM_SCHEMA,
                                            LightEntity)
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# # async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
# async def async_setup_entry(hass, config_entry, async_add_entities):
#     # #Создать объект с подключением к сервису
#     # sst1 = sst.SST(hass, entry.data["username"], entry.data["password"])
#     # hass.data.setdefault(DOMAIN, {})[entry.entry_id] = sst1
#     # await hass.async_add_executor_job(
#     #          sst1.pull_data
#     #      )
#     #
#     # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#     # return True
#     #
#     # sst1 = hass.data[DOMAIN][config_entry.entry_id]
#     # new_devices = []
#     # for module in sst1.devices:
#     #     if module.get_device_type == 7 or module.get_device_type == 2 or module.get_device_type == 4:
#     #         if module.get_device_type == 7:
#     #             new_devices.append(WaterSwitchFirstGroup(module))
#     #             if module.get_grouping == "two_groups":
#     #                 new_devices.append(WaterSwitchSecondGroup(module))
#     #         if module.get_device_type == 2 or module.get_device_type == 4:
#     #             new_devices.append(WaterSwitch(module))
#     #         new_devices.append((Washing_floors_mode(module)))
#
#     # device = SimpleLight(config_entry['url'], config_entry['port'])
#     device = SimpleLight('simple_light', 4444)
#     await async_add_entities([device])

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
})


def setup_platform(
        hass: HomeAssistant,
        config,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    # # Setup connection with devices/cloud
    # hub = awesomelights.Hub(host, username, password)
    #
    # # Verify that passed in configuration works
    # if not hub.is_valid_login():
    #     _LOGGER.error("Could not connect to AwesomeLight hub")
    #     return

    # Add devices
    light = SimpleLight(host, port)
    add_entities([light])


class SimpleLight(LightEntity):

    def __init__(self, url: str, port: int, default_state: bool = False):
        self._url = url
        self._port = port
        self._name = 'test_name'
        self._is_on = default_state
        pass

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the device on."""
        _LOGGER.info('start')
        r = requests.get(f'http://{self._url}:{self._port}/on')
        if not r.ok:
            _LOGGER.error('Cant\'t access to device')
        else:
            _LOGGER.info('successfully')

        self._is_on = self._convert_to_bool(r.text)

    def turn_off(self, **kwargs):
        """Turn the device off."""
        print('HHHUUUUUUIIIIIIIIIIIIII')
        _LOGGER.info('start')
        r = requests.get(f'http://{self._url}:{self._port}/off')
        if not r.ok:
            _LOGGER.error('Cant\'t access to device')
        else:
            _LOGGER.info('successfully')
        self._is_on = self._convert_to_bool(r.text)

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        print('HHHUUUUUUIIIIIIIIIIIIII')
        _LOGGER.info('start')
        r = requests.get(f'http://{self._url}:{self._port}/is_on')
        if not r.ok:
            _LOGGER.error('Cant\'t access to device')
        else:
            _LOGGER.info('successfully')
        self._is_on = self._convert_to_bool(r.text)

    def _convert_to_bool(self, arg: str) -> bool:
        if arg == 'True':
            return True
        else:
            return False

