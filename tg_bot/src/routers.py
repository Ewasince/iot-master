import logging
import os
from pathlib import Path

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.bot import bot


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу управлять тебе своим умным домом. Для этого отправь мне голосовое сообщение")


@router.message()
async def message_handler(msg: Message):
    """
        Обработчик получения голосового сообщения.
    """
    try:
        file_id = msg.voice.file_id
    except AttributeError:
        await msg.reply('Неверный формат сообщения')
        logger.info('Неверный формат сообщения')
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    await msg.reply("Аудио получено")

    # TODO ТУТ добавить распознование сообщение само сообщение лежит в file_on_disk
    # TODO Плюс запрос на апиху взависиомости от правильности распознного текста

    os.remove(file_on_disk)
