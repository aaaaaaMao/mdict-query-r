import unittest

from setup import temp_dir
from mocks import create_mdx
from mdict_query_r.query import Querier, Dictionary

class TestQuery(unittest.TestCase):
    def setUp(self):
        # Setup code to run before each test
        pass

    def tearDown(self):
        # Cleanup code to run after each test
        pass

    def test_query(self):
        mdx_file_path = f'{temp_dir}/test_querier.mdx'
        create_mdx(mdx_file_path)
        querier = Querier([Dictionary('test', mdx_file_path)])
        records = querier.query('doe')
        self.assertEqual(records, [
            {
                'dictionary': 'test',
                'record': 'a deer, a female deer.'
            }
        ])

if __name__ == '__main__':
    unittest.main()