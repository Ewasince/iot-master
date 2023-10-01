import os
import wave
from datetime import datetime

import pyaudio
import speech_recognition as sr

from project.config import config


def get_waw(seconds=3) -> str:
    try:
        # tmpdirname = tempfile.TemporaryDirectory(dir=temp_dir)
        # print('created temporary directory', tmpdirname)
        # filename = os.path.join(tmpdirname, str(time.time()), '.waw')

        filename = os.path.join(config.data_dir, str(datetime.now()) + '.wav')
        filename = filename.replace(':', ';')
        p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

        print(f'Recording ({seconds} seconds...')

        stream = p.open(format=config.sample_format,
                        channels=config.channels,
                        rate=config.rate,
                        frames_per_buffer=config.chunk,
                        input_device_index=1,  # индекс устройства с которого будет идти запись звука
                        input=True)

        frames = []  # Инициализировать массив для хранения кадров

        # Хранить данные в блоках в течение 3 секунд
        for i in range(0, int(config.rate / config.chunk * seconds)):
            data = stream.read(config.chunk)
            frames.append(data)

        # Остановить и закрыть поток
        stream.stop_stream()
        stream.close()
        # Завершить интерфейс PortAudio
        p.terminate()

        print('Finished recording!')

        # Сохранить записанные данные в виде файла WAV
        wf = wave.open(filename, 'wb')
        wf.setnchannels(config.channels)
        wf.setsampwidth(p.get_sample_size(config.sample_format))
        wf.setframerate(config.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        return filename
    except Exception as e:
        raise e
    finally:
        pass


def recognize_speech(filename: str) -> str:
    # print('try to recognize')
    # Создаем объект распознавателя речи
    recognizer = sr.Recognizer()

    # Загружаем аудио файл
    audio_file = sr.AudioFile(filename)

    # Распознаем речь из аудио файла
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='ru-RU')

    # Выводим текст
    return text
