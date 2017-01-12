import unittest
import functions

from metadata_profiles import profile_dict

core_xml = 'F:\\Projects\\python_transcoder\\tests\\metadata_test_source\\core_metadata.xml'
fd_xml = 'F:\\Projects\\python_transcoder\\tests\\metadata_test_source\\file_data.xml'
target = 'F:\\Projects\\python_transcoder\\tests\\metadata_test_source\\test.xml'


class MetadataCreation(unittest.TestCase):

    def test_1_create_metadata(self):
        profile_dict.metadata_profiles['amazon'](*functions.get_metadata(core_xml, fd_xml, target))

if __name__ == '__main__':
    unittest.main()
