import random
import string

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
