from voice_assistant.app_utils.config import Config
from voice_assistant.app_utils.utils import normalize_text, extract_text_after_command

from src.message_recognizers.i_messages_recognizer import IMyMessagesRecognizer
from src.message_recognizers.i_messages_source import IMyMessagesSource


class MessagesSourceTgBot(IMyMessagesSource):
    """Обрабатывает полученный текст от распознавателя"""

    def __init__(self, recognizer: IMyMessagesRecognizer):
        self.recognizer = recognizer
        self.config = Config()
        return

    def _prepare_text(self, input_text: str) -> str | None:
        text = normalize_text(input_text)

        filtered_text = extract_text_after_command(text, self.config.key_phase)

        if filtered_text is None:
            # print(f'text not contain phase: {text}')
            return

        return filtered_text

    def _check_command_after_key_word(self, text: str | None) -> str | None:
        if text is None:
            print("Ничего не услышал, слушаю дальше...")
            return

        filtered_text = self._prepare_text(text)
        if filtered_text is None:
            print(f"Не услышал ключевого слова: {text}")
            return

        if filtered_text == "":
            print(f"Не услышал ключевого слова: {text}")
            return

        return filtered_text

    async def get_text_from_audio(self, filename: str) -> str | None:
        text = await self.recognizer.get_text_from_audiofile(filename)

        command = self._check_command_after_key_word(text)

        return command
