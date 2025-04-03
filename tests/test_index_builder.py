import os
import time
import unittest

from setup import temp_dir
from index_builder import IndexBuilder
from lib.writemdict import MDictWriter

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/mock.mdx'
        db_file_path = self.mdx_file_path + '.db'
        if os.path.exists(db_file_path):
            os.remove(db_file_path)

        dictionary = {
            "doe": "a deer, a female deer.",
            "ray": "a drop of golden sun.",
            "me": "a name I call myself.",
            "far": "a long, long way to run."
        }
        writer = MDictWriter(
            dictionary, 
            title="Example Dictionary", 
            description="This is an example dictionary."
        )
        with open(self.mdx_file_path, 'wb') as f:
            writer.write(f)
    
    def test_init(self):
        builder = IndexBuilder(self.mdx_file_path)
    
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()