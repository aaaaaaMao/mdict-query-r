import unittest
import os
from time import time

from setup import mocks_dir
from mdict_query_r.db_manager import IndexManger

class TestIndexManger(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{mocks_dir}/index_manager_{int(time() * 1000)}.mdx'
        self.db_file_path = f'{self.mdx_file_path}.db'

        with open(self.mdx_file_path, 'w') as f:
            f.write('test')
            pass

        self.manager = None
    
    def test_init(self):
        self.manager = IndexManger(self.mdx_file_path)
        self.manager.db.close()

        self.manager = IndexManger(self.mdx_file_path)
        self.assertTrue(os.path.isfile(self.db_file_path))

    def test_rebuild(self):
        self.manager = IndexManger(self.mdx_file_path)
        self.manager.rebuild()
    
    def tearDown(self):
        if self.manager:
            self.manager.db.close()

if __name__ == '__main__':
    unittest.main()