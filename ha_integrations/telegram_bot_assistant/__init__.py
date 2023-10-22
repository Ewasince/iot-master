# """
# The "hello world" custom component.
#
# This component implements the bare minimum that a component should implement.
#
# Configuration:
#
# To use the telegram_bot_assistant component you will need to add the following to your
# configuration.yaml file.
#
# telegram_bot_assistant:
# """
# from __future__ import annotations
#
# import logging
# from typing import NoReturn
#
# from homeassistant.core import HomeAssistant
# from voice_assistant.app_interfaces.i_command_performer import ICommandPerformer
# from voice_assistant.app_interfaces.i_command_recognizer import ICommandRecognizer
# from voice_assistant.app_interfaces.i_messages_recognizer import IMessagesRecognizer
# from voice_assistant.app_interfaces.i_messages_source import IMessagesSource
# from voice_assistant.command_recognizer.simple.command_recognizer_simple import CommandRecognizerSimple
# from voice_assistant.commands.command_get_current_os.command_get_current_os import CommandGetCurrentOS
# from voice_assistant.commands.command_get_current_time.command_get_current_time import CommandGetCurrentTime
# from voice_assistant.massages_source.messages_source import MessagesSource
#
# from .recognizer.message_recognizer_local_files import MessageRecognizerLocalFiles
#
# _LOGGER = logging.getLogger(__name__)
#
# async def async_setup(hass: HomeAssistant, config):
#     """Set up component."""
#     _LOGGER.debug('a')
#     _LOGGER.info('a')
#     _LOGGER.warning('a')
#     _LOGGER.error('a')
#     _LOGGER.critical('start setup')
#     # Code for setting up your component inside of the event loop.
#     hass.states.async_set('telegram_bot_assistant.command_state', 'wait for a command')
#     hass.states.async_set('telegram_bot_assistant.last_message', '...')
#
#     # создаём объект распознавания голоса, который будет переводить наш голос в текст
#     messages_recognizer: IMessagesRecognizer = MessageRecognizerLocalFiles(hass)
#
#     # создаём объект источника команд, который будет предварительно обрабатывать команды
#     message_source: IMessagesSource = MessagesSource(messages_recognizer)
#
#     # создаём объект распознавания распознавателя команд
#     # на данный момент реализован только простой распознаватель команд
#     command_recognizer: ICommandRecognizer = CommandRecognizerSimple()
#
#     ### commands
#     # так же добавляем команды. Каждая команда – это класс, котрый должен реализовывать интерфейс
#
#     command_time: ICommandPerformer = CommandGetCurrentOS()
#     command_recognizer.add_command(command_time)
#
#     command_time: ICommandPerformer = CommandGetCurrentTime()
#     command_recognizer.add_command(command_time)
#
#     ### main process
#     # и, например, в цикле получаем от источника команд текстовые сообщения и обрабатываем их
#
#     _LOGGER.critical('init task')
#     hass.async_create_task(check_commands_cycle(message_source))
#     _LOGGER.critical('finish setup')
#
#     return True
#
# async def check_commands_cycle(message_source) -> NoReturn:
# # async def check_commands_cycle(message_source):
#
#     _LOGGER.critical('enter task')
#     while True:
#         _LOGGER.critical('wait command')
#         command = await message_source.wait_command()
#         # res = await command_recognizer.process_command(command)
#         _LOGGER.critical(f'process command! {command}')
#         break
#
#         # if command is not None:
#         #     hass.states.async_set('telegram_bot_assistant.last_message', command)
