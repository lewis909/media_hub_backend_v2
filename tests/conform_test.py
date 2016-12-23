import functions
import unittest


source_path = 'F:\\Projects\\python_transcoder\\tests\\conform_test_source\\'
one_part_test = source_path + '1_part_test.xml'
two_part_test = source_path + '2_part_test.xml'
three_part_test = source_path + '3_part_test.xml'
four_part_test = source_path + '4_part_test.xml'
conform_path = source_path
filename = 'test.mp4'


class ConformTest(unittest.TestCase):
    def test_1_part(self):
        conform_message, num_of_seg = functions.parse_xml(one_part_test, conform_path, filename)
        self.assertEqual(conform_message, 'ffmpeg -progress LOGFILE -i INPUT_FILE -ss 00:00:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_1_test.mp4')
        self.assertEqual(num_of_seg, 1)

    def test_2_parts(self):
        conform_message, num_of_seg = functions.parse_xml(two_part_test, conform_path, filename)
        num_of_parts_2 = 'ffmpeg -progress LOGFILE -i INPUT_FILE -ss 00:00:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_1_test.mp4 -ss 00:02:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_2_test.mp4'
        self.assertEqual(conform_message, num_of_parts_2)
        self.assertEqual(num_of_seg, 2)

    def test_3_parts(self):
        conform_message, num_of_seg = functions.parse_xml(three_part_test, conform_path, filename)
        num_of_parts_3 = 'ffmpeg -progress LOGFILE -i INPUT_FILE -ss 00:00:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_1_test.mp4 -ss 00:02:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_2_test.mp4 -ss 00:04:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_3_test.mp4'
        self.assertEqual(conform_message, num_of_parts_3)
        self.assertEqual(num_of_seg, 3)

    def test_4_parts(self):
        conform_message, num_of_seg = functions.parse_xml(four_part_test, conform_path, filename)
        num_of_parts_4 = 'ffmpeg -progress LOGFILE -i INPUT_FILE -ss 00:00:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_1_test.mp4 -ss 00:02:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_2_test.mp4 -ss 00:04:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_3_test.mp4 -ss 00:06:00.000 -t 00:01:00.000 F:\\\\Projects\\\\python_transcoder\\\\tests\\\\conform_test_source\\\\C_4_test.mp4'
        self.assertEqual(conform_message, num_of_parts_4)
        self.assertEqual(num_of_seg, 4)


if __name__ == '__main__':
    unittest.main()





