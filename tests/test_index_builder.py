import os
from time import time
import unittest

from setup import temp_dir, mocks_dir
from mocks import create_mdx, create_mdd
from mdict_query_r.index_builder import IndexBuilder
from mdict_query_r.mdict import Entry

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{mocks_dir}/index_builder_{int(time() * 1000)}.mdx'

        create_mdx(self.mdx_file_path)
        
        self.builder = None
    
    def test_init(self):
        self.builder = IndexBuilder(self.mdx_file_path)

        records = self.builder.query('doe')
        self.assertEqual(records, [
            Entry(id=1, key_text='doe', data='a deer, a female deer.')
        ])

        self.assertEqual(self.builder.headers['Title'], 'Example Dictionary')

    def test_rebuild(self):
        self.builder = IndexBuilder(self.mdx_file_path)
        self.builder.rebuild()

    def test_build_mdd_index(self):
        mdd_file_path = f'{mocks_dir}/basic.mdd'
        create_mdd(mdd_file_path, remove_db=True)

        builder = IndexBuilder(mdd_file_path)
        builder.index_manager.db.close()

    def test_query_keywords(self):
        self.builder = IndexBuilder(self.mdx_file_path)

        records = self.builder.query(keywords=['ray', 'far'])
        self.assertEqual(records, [
            Entry(id=2, key_text='far', data='a long, long way to run.'),
            Entry(id=4, key_text='ray', data='a drop of golden sun.'), 
        ])

    def test_query_ignore_case(self):
        self.builder = IndexBuilder(self.mdx_file_path)

        records = self.builder.query('RAY', ignore_case=True)
        self.assertEqual(records, [
            Entry(id=4, key_text='ray', data='a drop of golden sun.'), 
        ])

    def test_process_link_record(self):
        self.builder = IndexBuilder(self.mdx_file_path)
        records = self.builder.query('口内')
        self.assertEqual(records, [
            Entry(id=5, key_text='こうない【口内】', data='嘴裡。'), 
        ])

    @unittest.skip('local test')
    def test_build_large_mdict(self):
        mdx_file_path = f'{temp_dir}/プログレッシブ和英中辞典_v4.mdx'
        db_file_path = mdx_file_path + '.db'
        if os.path.exists(db_file_path):
            os.remove(db_file_path)

        builder = IndexBuilder(mdx_file_path)
        records = builder.query('心', ignore_case=True)
        self.assertGreater(len(records), 1)
    
    def tearDown(self):
        if self.builder:
            self.builder.index_manager.db.close()


if __name__ == '__main__':
    unittest.main()