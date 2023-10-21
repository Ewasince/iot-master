import logging

DOMAIN = "simple_light"

_logger = logging.getLogger(__name__)

def setup(hass, config):
    # hass.states.set(f"{DOMAIN}.world", "Paulus")
    #
    # _logger.info(f'setup!')
    #
    # # Return boolean to indicate that initialization was successful.
    return True