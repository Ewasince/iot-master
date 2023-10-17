from abc import ABC, abstractmethod


class IMessagesRecognizerMLM(ABC):

    @abstractmethod
    def get_audio(self) -> str:
        raise NotImplementedError
