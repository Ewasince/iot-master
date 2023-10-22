import os

import speech_recognition as sr

from src.config import Config
from src.message_recognizers.i_messages_recognizer import IMyMessagesRecognizer


class MessageRecognizerTgBot(IMyMessagesRecognizer):
    def __init__(self, config: Config, setup_micro=True):
        self.recognizer = sr.Recognizer()
        # self.microphone = sr.Microphone()
        # self.config = Config()
        #
        # if setup_micro:
        #     self.setup_microphone()

        self.config = config

        # self.websocket = connect(f"ws://{self.config.host}:{self.config.port}").__enter__()
        # self.websocket = connect(f"ws://{self.config.host}:{self.config.port}")

        pass

    async def get_text_from_audiofile(self, filename) -> str | None:
        # print("Слушаю...")
        # with self.microphone as source:
        #     audio = self.recognizer.listen(source)
        # # print("Got it! Now to recognize it...")
        # message = self.websocket.recv()
        # while True:
        #     filename = pop_from_order()
        #     if filename:
        #         break
        #     await asyncio.sleep(3)

        filename = os.path.join(self.config.voice_files_directory, filename)

        text = await self.recognize_from_file(filename)
        return text

    async def recognize_speech(self, audio_data: sr.AudioData) -> str | None:
        # Распознаем речь из аудио
        try:
            value = self.recognizer.recognize_google(
                audio_data, language=self.config.language
            )

            # print("You said {}".format(value))
        except sr.UnknownValueError:
            # print("Oops! Didn't catch that")
            return None
        except sr.RequestError as e:
            print(
                f"Couldn't request results from Google Speech Recognition service; {e}"
            )
            raise e
        else:
            return value

    async def recognize_from_file(self, audio_filename: str) -> str:
        # Загружаем аудио файл
        audio_file = sr.AudioFile(audio_filename)

        with audio_file as source:
            audio_data = self.recognizer.record(source)
            text = await self.recognize_speech(audio_data)

        return text
