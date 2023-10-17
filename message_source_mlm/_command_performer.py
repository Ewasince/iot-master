from typing import Callable

from message_source_mlm.interfaces.i_command_performer_mlm import ICommandPerformerMLM
from message_source_mlm.utils import extract_text_after_command


class CommandPerformerMLM(ICommandPerformerMLM):
    def __init__(self):
        self._command_dict: dict[str, Callable[[str], None]] = {}
        return

    def add_command(self, command: str, callback: Callable[[], None]):
        self._command_dict[command] = callback
        return

    def delete_command(self, command: str):
        del self._command_dict[command]
        return

    def perform_command(self, text: str):
        for command, action in self._command_dict.items():
            if command not in text:
                continue
            filtered_text = extract_text_after_command(text, command)
            action(filtered_text)
            return

        return
