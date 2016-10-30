import os
import base64
from functools import partial
from Crypto.Cipher import AES, Blowfish
import uuid

try:
    from md5 import md5 as hash_func
except ImportError:
    from hashlib import md5 as hash_func

import json
from copy import deepcopy



b64e = lambda s: base64.b64encode(s).rstrip()
b64d = base64.b64decode


def _cipher(algo, secret):
    h = hash_func()
    h.update(secret)
    hash_line = h.hexdigest()

    l = len(secret)
    if l < 32:
        secret = secret + hash_line[l:]
    else:
        secret = secret[:32]
    return algo.new(secret)

aes = partial(_cipher, AES)
blowfish = partial(_cipher, Blowfish)


def pack(data):
    data = b64e(data)
    m = len(data) % 16
    return data + (16 - m) * '~'


def unpack(data):
    return b64d(data.rstrip('~'))


def encode(cipher, data):
    return b64e(cipher.encrypt(pack(data))).replace('\n','')


def decode(cipher, data):
    return unpack(cipher.decrypt(b64d(data)))


def parse_record(data):
    return tuple([b64d(r) for r in data.split(',')])


def build_record(name, user, password, keywords):
    return b64e(name), b64e(user), b64e(password), b64e(keywords)

# cipher order:
# save: text -> b64e -> append ~~~ -> encrypt -> b64e
# load: b64d -> decrypt -> rstrip ~~~ -> b64d -> text

class PasswordError(Exception):
    pass

class SafeStorageOld:
    #NOTE. record fields: name, user, password, keywords
    def __init__(self, db, passwd):
        self._file_db = db
        #aes and blowfish ciphers
        self._aes = aes(passwd)
        self._blowfish = blowfish(passwd)

        mode = 'r' if os.path.exists(db) else 'w+'

        self._map = []
        with open(self._file_db, mode) as f:
            for line in f.readlines():
                if line:
                    try:
                        self._map.append(
                            parse_record(
                                decode(self._aes, line.rstrip())))
                    except Exception:
                        raise PasswordError

    @property
    def file_path(self):
        return self._file_db

    def close(self):
        pass

    def get_records(self, indx_list, with_passwords=False):
        result = [self._map[i] for i in indx_list]
        if with_passwords:
            return [(i[0],i[1],decode(self._blowfish,i[2]),i[3]) for i in result]
        return [(i[0],i[1],'******',i[3]) for i in result]

    def get_record(self, indx, with_passwords=False):
        i = self._map[indx]
        if with_passwords:
            return i[0], i[1], decode(self._blowfish, i[2]), i[3]
        return i[0], i[1], '******', i[3]

    def search(self, word):
        result = []
        for i, record in enumerate(self._map):
            if any(word in item for item in record) or word == str(i):
                result.append(i)
        return result

    def add(self, name, user, password, keywords):
        password = encode(self._blowfish, password)
        builded = ','.join(build_record(name, user, password, keywords))
        encoded = encode(self._aes, builded)
        self._map.append((name, user, password, keywords))
        #saving to file
        with open(self._file_db, 'a') as f:
            f.write(encoded)
            f.write('\n')

    def edit(self, indx, record):
        self._map[indx] = (record[0],record[1],encode(self._blowfish,record[2]),record[3])
        self._resave()

    def delete(self, indx):
        self._map.pop(indx)
        self._resave()
    
    def change_password(self, password):
        new_records = []
        new_aes = aes(password)
        new_blowfish = blowfish(password)

        for (name,user,passwd,kw) in self._map:
            p = decode(self._blowfish, passwd)
            passwd = encode(new_blowfish, p)
            new_records.append((name, user, passwd, kw))

        #atomic{
        self._aes = new_aes
        self._blowfish = new_blowfish
        self._map = new_records
        self._resave()
        #}

    def _resave(self):
        with open(self._file_db,'w') as f:
            f.truncate()
            for record in self._map:
                builded = ','.join(build_record(*record))
                encoded = encode(self._aes, builded)
                f.write(encoded)
                f.write('\n')


class Record(dict):
    version = 1
    columns = ('id', 'title', 'user', 'secret', 'keywords')
    editable_columns = ('title', 'user', 'secret', 'keywords')
    secret_columns = ('user', 'secret')

    @property
    def id(self):
        return self['id']

    def copy_record(self, strip_secret=False):
        r = deepcopy(self)
        if strip_secret:
            for c in self.secret_columns:
                r[c] = '***{}***'.format(c)
        return r


class SafeStorage:
    record_class = Record

    def __init__(self, path, master_password):
        self._path = path
        self._db = self._open(path, master_password)

    def _open(self, path, master_password):
        # TODO. open with master password (so entire file is ciphered)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('[]')

        data = []
        with open(path) as f:
            for entry in json.load(f):
                data.append(self.record_class(**entry))

        return list(sorted(data, key=lambda obj: obj['id']))

    def _sync(self):
        with open(self._path, 'w') as f:
            json.dump(self._db, f)

    def close(self):
        self._sync()

    @property
    def file_path(self):
        return self._path

    def get_records(self, ids_list, strip_secret=False):
        return [r.copy_record(strip_secret=strip_secret)
                for r in self._db if r.id in ids_list]

    def get_record(self, record_id, strip_secret=False):
        return next(iter(self.get_records([record_id], strip_secret=strip_secret)), None)

    def search(self, word):
        result = []
        for record in self._db:
            if any(word in item for item in record.values()):
                result.append(record.id)
        return result

    def add(self, **data):
        record = self.record_class(id=uuid.uuid4().hex, **data)
        self._db.append(record)
        return record

    def edit(self, record_id, new_record):
        for record in self._db:
            if record.id == record_id:
                record.update(new_record)

        self._sync()

    def delete(self, record_id):
        self._db = [r for r in self._db if r.id != record_id]
        self._sync()

    def change_password(self, password):
        new_records = []
        new_aes = aes(password)
        new_blowfish = blowfish(password)

        for (name,user,passwd,kw) in self._map:
            p = decode(self._blowfish, passwd)
            passwd = encode(new_blowfish, p)
            new_records.append((name, user, passwd, kw))

        #atomic{
        self._aes = new_aes
        self._blowfish = new_blowfish
        self._map = new_records
        self._resave()
        #}
