import os
import random
import string
import shutil
from datetime import datetime


DEFAULT_CHARSET = string.ascii_letters + string.digits
DEFAULT_PASSWORD_LENGTH = 10


def generate_password(length=DEFAULT_PASSWORD_LENGTH, charset=string.ascii_letters + string.digits):
    charset = charset or DEFAULT_CHARSET
    length = length or DEFAULT_PASSWORD_LENGTH
    range_dict = {
        'a-z': string.ascii_lowercase,
        'A-Z': string.ascii_uppercase,
        '0-9': string.digits,
        '$$': string.punctuation,
    }

    for k, v in range_dict.items():
        charset = charset.replace(k, v)

    return ''.join(random.choice(charset) for __ in range(length))


def get_real_path(path):
    if os.path.islink(path):
        return os.readlink(path)
    return os.path.realpath(path)


def get_dir(path):
    return os.path.dirname(get_real_path(path))


def backup_file(path, dst=''):
    path = get_real_path(path)
    dst = get_real_path(dst) if dst else ''
    file_path = lambda dir: os.path.join(dir, datetime.now().strftime('.safep.%Y-%m-%d-%H%M%S'))

    if not dst:
        dst = file_path(get_dir(path))
    elif os.path.isdir(dst):
        dst = file_path(dst)
    shutil.copy(path, dst)
    return os.path.exists(dst)


def backups_list(path):
    path_folder = get_dir(path)
    full_dir = lambda f: os.path.join(path_folder, f)
    return reversed(sorted((f,full_dir(f)) for f in os.listdir(path_folder) if f.startswith('.safep.') and os.path.isfile(full_dir(f))))



