import logging
import os
from pathlib import Path

import soundfile as sf
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from voice_assistant import CommandRecognizer

from src.config import Config
from src.message_recognizers.i_messages_source import IMyMessagesSource

logger = logging.getLogger(__name__)


class RouterWrapper:
    def __init__(
        self,
        message_source: IMyMessagesSource,
        command_recognizer: CommandRecognizer,
        bot: Bot,
    ):
        router = Router()

        self.config = Config()
        self.router = router
        self.bot = bot
        self.message_source = message_source
        self.command_recognizer = command_recognizer

        router.message.register(self.start_handler, Command("start"))
        router.message.register(self.message_handler)
        return

    async def message_handler(self, msg: Message):
        """
        Обработчик получения сообщений.
        """
        try:
            msg.voice.file_id
        except AttributeError:
            await self._perform_iot_command(msg.text, msg)
            return
        else:
            await self._voice_message_handler(msg)

    async def _voice_message_handler(self, msg: Message):
        file_id = msg.voice.file_id

        file_on_disk_oga = None
        file_on_disk_wav = None

        try:
            # get audio file from tg
            file = await self.bot.get_file(file_id)
            file_name_oga = f"{file_id}.oga"
            file_on_disk_oga = Path(self.config.voice_files_directory, file_name_oga)

            await self.bot.download_file(file.file_path, destination=file_on_disk_oga)
            await msg.reply("Аудио получено")

            # convert audio to wav
            file_name_wav = f"{file_id}.wav"
            file_on_disk_wav = Path(self.config.voice_files_directory, file_name_wav)

            data, samplerate = sf.read(file_on_disk_oga)
            sf.write(file_on_disk_wav, data, samplerate)

            # process text from audio
            command = await self.message_source.get_text_from_audio(file_name_wav)

            if command is None:
                return

            await self._perform_iot_command(command, msg)
        finally:
            # if file_on_disk_oga: os.remove(file_on_disk_oga)
            if file_on_disk_wav:
                os.remove(file_on_disk_wav)
            pass

    async def _perform_iot_command(self, command: str, msg: Message):
        res = await self.command_recognizer.process_command(command)

        if res is None:
            return

        await msg.reply(res)

    async def start_handler(self, msg: Message):
        await msg.answer(
            "Привет! Я помогу управлять тебе своим умным домом. Для этого отправь мне голосовое сообщение"
        )
