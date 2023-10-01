import os
from datetime import datetime


def get_current_time():
    cur_time = datetime.now()
    print(cur_time)
    return

def get_os_type():
    os_type = os.name
    print(os_type)
