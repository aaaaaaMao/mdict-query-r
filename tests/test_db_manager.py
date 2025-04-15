import unittest
import os
from time import time

from setup import temp_dir
from mdict_query_r.db_manager import IndexManger

class TestMdxIndexManger(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/im_mock_{int(time() * 1000)}.mdx'
        self.db_file_path = f'{self.mdx_file_path}.db'
        with open(self.mdx_file_path, 'w') as f:
            f.write('test')
            pass
    
    def test_init(self):
        manager = IndexManger(self.mdx_file_path)
        manager.db.close()

        manager2 = IndexManger(self.mdx_file_path)
        self.assertTrue(os.path.isfile(self.db_file_path))
        manager2.db.close()

    def test_rebuild(self):
        manager = IndexManger(self.mdx_file_path)
        manager.rebuild()
        manager.db.close()
    
    def tearDown(self):
        for filepath in [self.mdx_file_path, self.db_file_path]:
            if os.path.exists(filepath):
                os.remove(filepath)

if __name__ == '__main__':
    unittest.main()