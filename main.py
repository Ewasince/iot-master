import os.path
import re
# import tempfile
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import pyaudio
import wave
import speech_recognition as sr

chunk = 1024  # Запись кусками по 1024 сэмпла
sample_format = pyaudio.paInt16  # 16 бит на выборку
channels = 2
rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
root_temp_dir = 'tmp'

key_phase = 'hello hello'

if not os.path.exists(root_temp_dir):
    os.makedirs(root_temp_dir)


def get_waw(seconds=3) -> str:
    tmpdirname = root_temp_dir

    try:
        # tmpdirname = tempfile.TemporaryDirectory(dir=temp_dir)
        # print('created temporary directory', tmpdirname)
        # filename = os.path.join(tmpdirname, str(time.time()), '.waw')

        filename = os.path.join(root_temp_dir, str(datetime.now()) + '.wav')
        filename = filename.replace(':', ';')
        p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

        print(f'Recording ({seconds} seconds...')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=rate,
                        frames_per_buffer=chunk,
                        input_device_index=1,  # индекс устройства с которого будет идти запись звука
                        input=True)

        frames = []  # Инициализировать массив для хранения кадров

        # Хранить данные в блоках в течение 3 секунд
        for i in range(0, int(rate / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Остановить и закрыть поток
        stream.stop_stream()
        stream.close()
        # Завершить интерфейс PortAudio
        p.terminate()

        print('Finished recording!')

        # Сохранить записанные данные в виде файла WAV
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
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


def get_sound_devices():
    """Выдает список девайсов для записи аудио"""
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_name: str = p.get_device_info_by_index(i)['name']
        device_name = device_name.encode('cp1251').decode('utf-8')
        print(i, device_name)


if __name__ == '__main__':

    # # для тестирования записи и распознавания
    # audio_filename = get_waw(5)
    # text = recognize_speech(audio_filename)
    # print(text)

    # while True:

    # паттерн для удалени спец символов
    p = re.compile('[^A-Za-zА-Яа-я0-9 ]')

    def check_speech_after_word():
        audio_filename = get_waw(5)
        text = recognize_speech(audio_filename)
        text = text.lower()
        text = p.sub('', text)

        pos = text.find(key_phase)
        if pos == -1:
            print(f'text not contain phase: {text}')
            return

        pos = pos + len(key_phase)

        print(text[pos:])

        pass


    check_speech_after_word()

    # sched = BackgroundScheduler()
    # sched.add_job(
    #
    # )
    pass
