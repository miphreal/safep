import os
import random
import string
import shutil
from datetime import datetime

DEFAULT_CHARSET = string.letters+string.digits


def generate_password(length=10, charset=string.letters+string.digits):
    charset = charset or DEFAULT_CHARSET
    length = length or 10
    range_dict = {
        'a-z': string.lowercase,
        'A-Z': string.uppercase,
        '0-9': string.digits,
        '$$': string.punctuation,
    }

    for k, v in range_dict.items():
        charset = charset.replace(k, v)

    rand_char = lambda: charset[random.randrange(0, len(charset))]
    passwd = ''.join(rand_char() for i in xrange(length))

    return passwd

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
    dir = get_dir(path)
    full_dir = lambda f: os.path.join(dir, f)
    return reversed(sorted((f,full_dir(f)) for f in os.listdir(dir) if f.startswith('.safep.') and os.path.isfile(full_dir(f))))



