from abc import ABC, abstractmethod


class IMyMessagesRecognizer(ABC):
    """Определяет интерфейс класса, который выдаёт расшифрованный текст"""

    @abstractmethod
    async def get_text_from_audiofile(self, filename: str) -> str | None:
        """Выдаёт текст сообщенмия и блокирует данный контекст исполнения пока не выдаст текст расшифрованного сообщения"""
        raise NotImplementedError
