from src.devices.utils import perform_request


class Light:
    def __init__(self, name, url_on, url_off):
        self.name = name
        self.url_on = url_on
        self.url_off = url_off

    async def turn_on(self) -> bool:
        return await perform_request(self.url_on)

    async def turn_off(self) -> bool:
        return await perform_request(self.url_off)
