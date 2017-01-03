import config
import unittest


class DbConnectionTest(unittest.TestCase):

    def test_1_db_access(self):
        test_query = "SELECT * FROM media_hub.users WHERE username='admin'"
        config.cursor_1.execute(test_query)
        result = config.cursor_1.fetchall()[0][1]
        self.assertEqual(result, 'admin')

if __name__ == '__main__':
    unittest.main()
