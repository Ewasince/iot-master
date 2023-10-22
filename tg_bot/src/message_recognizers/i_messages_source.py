from abc import ABC, abstractmethod


class IMyMessagesSource(ABC):
    """Определяет интерфейс класса, который выдаёт нормализованный текст, содержащий команду"""

    @abstractmethod
    async def get_text_from_audio(self, filename: str) -> str | None:
        """Вызывается для получения следующего текста с командами и возвращает его, когда таковой будет получен"""
        raise NotImplementedError
