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

def create_mdd(filepath: str, data: dict={}, remove_db=False):
    db_file_path = filepath + '.db'
    if remove_db and os.path.exists(db_file_path):
        os.remove(db_file_path)

    # A raw PNG file, with size 10x10, all red.
    raw_image = (b"\x89PNG\r\n\x1a\n"
                b"\0\0\0\x0dIHDR"
                b"\0\0\0\x0a\0\0\0\x0a\x08\x02\x00\x00\x00"
                b"\x02\x50\x58\xea"
                b"\x00\x00\x00\x12IDAT"
                b"\x18\xd3\x63\xfc\xcf\x80\x0f\x30\x31\x8c\x4a\x63\x01\x00\x41\x2c\x01\x13"
                b"\x65\x62\x10\x33"
                b"\0\0\0\0IEND"
                b"\xae\x42\x60\x82")
        
    data = {"\\red.png": raw_image}
    data.update(data)

    writer = MDictWriter(
        data, 
        title="Dictionary with MDD file", 
        description="This dictionary tests MDD file handling.",
        is_mdd=True
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
    
    def test_build_mdd_index(self):
        mdd_file_path = f'{temp_dir}/basic.mdd'
        create_mdd(mdd_file_path, remove_db=True)

        builder = IndexBuilder(mdd_file_path)

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