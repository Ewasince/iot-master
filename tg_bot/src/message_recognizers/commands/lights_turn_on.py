from voice_assistant.app_interfaces.i_command_performer import ICommandPerformer

from src.devices.light import Light
from src.message_recognizers.commands.utils import prepare_light_name


class CommandLightsTurnOn(ICommandPerformer):
    def __init__(self, light_list: list[Light]):
        self._lights = light_list

    def get_command_topic(self) -> str:
        return "включи лампочку"

    async def perform_command(self, command_context: str) -> str | None:
        # extract_text_after_command(command_context, self.get_command_text())
        for light in self._lights:
            light_name = prepare_light_name(light.name)
            possible_light_name = prepare_light_name(command_context)
            if light_name != possible_light_name:
                continue
            break
        else:
            return f'Не нашёл лампочки с названием "{command_context}"'

        res = await light.turn_on()

        if res:
            return f'Лампочка "{light.name}" успешно включена'
        else:
            return f'Не удалось включить лампочку "{light.name}'
