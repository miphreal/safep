import unittest

from safep import storage


class MyTestCase(unittest.TestCase):
    def test_pack_unpack(self):
        for data in ('some data', 'sd',
                     'sooooooooooooooooome daaaaaaaaaaaaaataaaaaaaaaaaaaaaaa'):
            pack_data = storage.pack(data)
            self.assertEqual(data, storage.unpack(pack_data))

    def test_encode_decode(self):
        for cipher in (storage.aes, storage.blowfish):
            c = cipher('pass')
            for data in ('some data', 'sd',
                         'sooooooooooooooooome daaaaaaaaaaaaaataaaaaaaaaaaaaaaaa'):
                encode_data = storage.encode(c, data)
                self.assertEqual(data, storage.decode(c, encode_data))

    def test_parse_build(self):
        data = ('record name','miphreal','my pass','kw, test; hi')
        b = storage.build_record(*data)
        self.assertTupleEqual(data, storage.parse_record(','.join(b)))


if __name__ == '__main__':
    unittest.main()
