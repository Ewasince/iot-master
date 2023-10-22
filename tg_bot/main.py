import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from voice_assistant import CommandRecognizer
from voice_assistant.app_interfaces import ITopicDefiner
from voice_assistant.app_interfaces.i_command_performer import ICommandPerformer
from voice_assistant.commands.test_commands.get_current_os import CommandGetCurrentOS
from voice_assistant.commands.test_commands.get_current_time import (
    CommandGetCurrentTime,
)
from voice_assistant.topic_definers.simple.simple import TopicDefinerSimple

from src.config import Config
from src.message_recognizers.commands.lights_turn_off import CommandLightsTurnOff
from src.message_recognizers.commands.lights_turn_on import CommandLightsTurnOn
from src.message_recognizers.i_messages_recognizer import IMyMessagesRecognizer
from src.message_recognizers.i_messages_source import IMyMessagesSource
from src.message_recognizers.message_recognizer_tg_bot import MessageRecognizerTgBot
from src.message_recognizers.message_source import MessagesSourceTgBot
from src.routers import RouterWrapper


async def main():
    config = Config()

    # создаём объект распознавания голоса, который будет переводить наш голос в текст
    messages_recognizer: IMyMessagesRecognizer = MessageRecognizerTgBot(config)

    # создаём объект источника команд, который будет предварительно обрабатывать команды
    message_source: IMyMessagesSource = MessagesSourceTgBot(messages_recognizer)

    # создаём объект распознавания распознавателя команд
    # на данный момент реализован только простой распознаватель команд
    topic_definer: ITopicDefiner = TopicDefinerSimple()
    command_recognizer = CommandRecognizer(topic_definer)

    ### commands
    # так же добавляем команды. Каждая команда – это класс, котрый должен реализовывать интерфейс
    command_time: ICommandPerformer = CommandGetCurrentOS()
    command_recognizer.add_command(command_time)

    command_os: ICommandPerformer = CommandGetCurrentTime()
    command_recognizer.add_command(command_os)

    command_lights_turn_on: ICommandPerformer = CommandLightsTurnOn(
        config.devices["lights"]
    )
    command_recognizer.add_command(command_lights_turn_on)

    command_lights_turn_on: ICommandPerformer = CommandLightsTurnOff(
        config.devices["lights"]
    )
    command_recognizer.add_command(command_lights_turn_on)

    # setup bot
    bot = Bot(token=Config().token)
    my_router = RouterWrapper(message_source, command_recognizer, bot)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(my_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
