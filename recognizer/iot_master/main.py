from typing import NoReturn

from recognizer.app_interfaces.i_command_performer import ICommandPerformer
from recognizer.app_interfaces.i_command_recognizer import ICommandRecognizer
from recognizer.app_interfaces.i_messages_recognizer import IMessagesRecognizer
from recognizer.app_interfaces.i_messages_source import IMessagesSource
from recognizer.command_recognizer.command_recognizer_simple import CommandRecognizerSimple
from recognizer.commands.command_get_current_os.command_get_current_os import CommandGetCurrentOS
from recognizer.commands.command_get_current_time.command_get_current_time import (
    CommandGetCurrentTime,
)
from recognizer.massages_source.messages_source import MessagesSourceLocalMic
from recognizer.message_recognizer_local_mic.message_recognizer_local_mic import (
    MessageRecognizerLocalMic,
)


def main() -> NoReturn:
    messages_recognizer: IMessagesRecognizer = MessageRecognizerLocalMic()
    message_source: IMessagesSource = MessagesSourceLocalMic(messages_recognizer)

    command_recognizer: ICommandRecognizer = CommandRecognizerSimple()

    ### commands

    command_time: ICommandPerformer = CommandGetCurrentOS()
    command_recognizer.add_command(command_time)

    command_time: ICommandPerformer = CommandGetCurrentTime()
    command_recognizer.add_command(command_time)

    ### main process

    while True:
        command = message_source.wait_command()
        res = command_recognizer.process_command(command)

        if res is not None:
            print(res)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Поставьте 5!")
