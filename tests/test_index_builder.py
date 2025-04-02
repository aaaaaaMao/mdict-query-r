import os
import unittest

from setup import temp_dir
from index_builder import IndexBuilder

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/プログレッシブ和英中辞典_v4.mdx'
        os.remove(self.mdx_file_path + '.db')
    
    def test_init(self):
        builder = IndexBuilder(self.mdx_file_path)
    
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()