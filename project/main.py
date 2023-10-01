import os.path
import re
# import tempfile
from typing import NoReturn

import pyaudio

from project.audio import get_waw, recognize_speech
from project.command_performer import CommandPerformer
from project.commands import get_current_time, get_os_type
from project.config import config
from project.utils import extract_text_after_command


def test_audio():
    def get_sound_devices():
        """Выдает список девайсов для записи аудио"""
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            device_name: str = p.get_device_info_by_index(i)['name']
            device_name = device_name.encode('cp1251').decode('utf-8')
            print(i, device_name)

    get_sound_devices()

    # для тестирования записи и распознавания
    audio_filename = get_waw(5)
    text = recognize_speech(audio_filename)
    print(text)
    return


def prepare_text(input_text: str) -> str | None:
    text = input_text.lower()
    text = p.sub('', text)

    filtered_text = extract_text_after_command(text, config.key_phase)

    if filtered_text is None:
        print(f'text not contain phase: {text}')
        return

    print(filtered_text)
    return filtered_text


def main() -> NoReturn:
    command_performer = CommandPerformer()
    command_performer.add_command('время', get_current_time)
    command_performer.add_command('система', get_os_type)

    def check_speech_after_word():
        audio_filename = get_waw(5)
        text = recognize_speech(audio_filename)
        text = prepare_text(text)
        if text:
            command_performer.perform_command(text)
        return

    check_speech_after_word()

    # sched = BackgroundScheduler()
    # sched.add_job(
    #
    # )
    pass


if __name__ == '__main__':
    p = re.compile(config.regexp)

    if not os.path.exists(config.data_dir):
        os.makedirs(config.data_dir)

    main()
