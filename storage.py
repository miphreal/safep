__author__ = 'miph'


import base64
b64e = base64.encodestring
b64d = base64.decodestring

from functools import partial
from Crypto.Cipher import AES, Blowfish

try:
    from md5 import md5 as hash_func
except ImportError:
    from hashlib import md5 as hash_func




def half(s):
    l = len(s)/2
    return s[:l], s[l:]


def cipher(algo, secret):
    h = hash_func()
    h.update(secret)
    hash = h.hexdigest()

    l = len(secret)
    if l<32:
        secret = secret+hash[l:]
    else:
        secret = secret[:32]
    return algo.new(secret)

aes = partial(cipher, AES)
blowfish = partial(cipher, Blowfish)


def pack(data):
    data = b64e(data).rstrip()
    m = len(data) % 16
    return data + (16-m)*'~'

def unpack(data):
    return b64d(data.rstrip('~'))

def encode(cipher, data):
    return cipher.encrypt(pack(data))

def decode(cipher, data):
    return unpack(cipher.decrypt(data))


class SafeStorage:
    #NOTE. record fields: name, user, password, keywords
    def __init__(self, db, passwd):
        self._file_db = db
        h = hash_func()
        h.update(passwd)
        self._hash = h.hexdigest()
        #open db
        blf, aes = half(self._hash)
        cipher = Blowfish.new(blf)
        with open(self._file_db,'r') as f:
            for line in f.readlines():
                pass

    def close(self):
        pass

    def search(self):
        pass

    def add(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass
    
    def change_password(self):
        pass