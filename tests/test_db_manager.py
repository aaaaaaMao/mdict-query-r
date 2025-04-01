import unittest
import os
from time import time

from setup import temp_dir
from db_manager import MdxIndexManger

class TestMdxIndexManger(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/mock_{int(time() * 1000)}.mdx'
        self.db_file_path = f'{self.mdx_file_path}.db'
        with open(self.mdx_file_path, 'w') as f:
            pass
    
    def test_init(self):
        manager = MdxIndexManger(self.mdx_file_path)
        manager.db.close()

        manager2 = MdxIndexManger(self.mdx_file_path)
        self.assertTrue(os.path.isfile(self.db_file_path))
        manager2.db.close()
    
    def tearDown(self):
        os.remove(self.mdx_file_path)
        os.remove(self.db_file_path)


if __name__ == '__main__':
    unittest.main()