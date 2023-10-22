import asyncio
import os

import speech_recognition as sr
from homeassistant.core import HomeAssistant
from voice_assistant.app_interfaces.i_message_recognizer import IMessageRecognizer

from .dummy_config import Config


class MessageRecognizerLocalFiles(IMessageRecognizer):

    def __init__(self, hass: HomeAssistant, setup_micro=True, config=Config):
        self.recognizer = sr.Recognizer()
        # self.microphone = sr.Microphone()
        # self.config = Config()
        #
        # if setup_micro:
        #     self.setup_microphone()

        self.config = config
        self.hass = hass

        # self.websocket = connect(f"ws://{self.config.host}:{self.config.port}").__enter__()
        # self.websocket = connect(f"ws://{self.config.host}:{self.config.port}")

        pass

    async def get_audio(self) -> str | None:
        print("Слушаю...")
        # with self.microphone as source:
        #     audio = self.recognizer.listen(source)
        # # print("Got it! Now to recognize it...")
        # message = self.websocket.recv()
        await asyncio.sleep(5)
        message = 'test.wav'

        filename = os.path.join(self.config.voice_files_directory, message)

        text = await self.recognize_from_file(filename)
        return text

    async def recognize_speech(self, audio_data: sr.AudioData) -> str | None:
        # Распознаем речь из аудио
        try:
            # recognize speech using Google Speech Recognition
            value = await self.hass.async_add_executor_job(
                self.pipiska,
                audio_data, self.config.language
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

    def pipiska(self, audio_data, language) -> str | None:
        res = self.recognizer.recognize_google(audio_data, language=language)
        return res
