import os
from threading import Thread
from time import sleep

from flask import Flask

app = Flask(__name__)

DEBUG_MODE = os.environ.get("DEBUG", True)
APP_PORT = os.environ.get("DEBUG", 4444)
APP_HOST = os.environ.get("DEBUG", "0.0.0.0")

is_on_state = False


@app.route('/on')
def on():
    global is_on_state
    is_on_state = True
    return str(is_on_state)


@app.route('/off')
def off():
    global is_on_state
    is_on_state = False
    return str(is_on_state)


@app.route('/is_on')
def is_on():
    return str(is_on_state)


def say_about_state():
    while True:
        if is_on_state:
            print('Ligth ☀️')
        else:
            print('Dark 🌑️')
        sleep(3)


if __name__ == '__main__':
    t = Thread(target=say_about_state)
    t.start()

    app.run(APP_HOST, APP_PORT)
