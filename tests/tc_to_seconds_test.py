import functions
import unittest


class TcToSeconds(unittest.TestCase):

    def test_1(self):
        tc_source = '00:10:00.00'
        timecode = tc_source.split(':')
        self.assertEqual(functions.timecode_to_secs(*timecode), 600)

    def test_2(self):
        tc_source = '01:00:00.00'
        timecode = tc_source.split(':')
        self.assertEqual(functions.timecode_to_secs(*timecode), 3600)

    def test_3(self):
        tc_source = '02:37:12.00'
        timecode = tc_source.split(':')
        self.assertEqual(functions.timecode_to_secs(*timecode), 9432)

    def test_4(self):
        tc_source = '05:59:59.00'
        timecode = tc_source.split(':')
        self.assertEqual(functions.timecode_to_secs(*timecode), 21599)

if __name__ == '__main__':
    unittest.main()
