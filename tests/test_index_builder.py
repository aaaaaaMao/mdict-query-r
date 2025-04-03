import os
from time import time
import unittest

from setup import temp_dir
from index_builder import IndexBuilder
from lib.writemdict import MDictWriter

def create_mdx(filepath: str, data: dict={}, remove_db=False):
    db_file_path = filepath + '.db'
    if remove_db and os.path.exists(db_file_path):
        os.remove(db_file_path)
    
    dictionary = {
        "doe": "a deer, a female deer.",
        "ray": "a drop of golden sun.",
        "me": "a name I call myself.",
        "far": "a long, long way to run.",
    }
    dictionary.update(data)

    writer = MDictWriter(
        dictionary, 
        title="Example Dictionary", 
        description="This is an example dictionary."
    )
    with open(filepath, 'wb') as f:
        writer.write(f)

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/index_builder_{int(time() * 1000)}.mdx'
        self.db_file_path = self.mdx_file_path + '.db'

        create_mdx(self.mdx_file_path)
    
    def test_init(self):
        mdx_file_path = f'{temp_dir}/basic.mdx'
        create_mdx(mdx_file_path, remove_db=True)

        builder = IndexBuilder(mdx_file_path)

        records = builder.query('doe')
        self.assertEqual(records, [
            'a deer, a female deer.'
        ])

    def test_query_keywords(self):
        builder = IndexBuilder(self.mdx_file_path)

        records = builder.query(keywords=['ray', 'far'])
        self.assertEqual(records, [
            'a long, long way to run.',
            'a drop of golden sun.'
        ])

        builder.index_manager.db.close()

    def test_query_ignore_case(self):
        builder = IndexBuilder(self.mdx_file_path)

        records = builder.query('RAY', ignore_case=True)
        self.assertEqual(records, [
            'a drop of golden sun.'
        ])

        builder.index_manager.db.close()
    
    def tearDown(self):
        os.remove(self.mdx_file_path)
        if os.path.exists(self.db_file_path):
            os.remove(self.db_file_path)


if __name__ == '__main__':
    unittest.main()