import os
from time import time
import unittest

from setup import temp_dir
from mocks import create_mdx, create_mdd
from mdict_query_r.index_builder import IndexBuilder

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.mdx_file_path = f'{temp_dir}/index_builder_{int(time() * 1000)}.mdx'
        self.db_file_path = self.mdx_file_path + '.db'

        create_mdx(self.mdx_file_path)
        
        self.builder = None
    
    def test_init(self):
        mdx_file_path = f'{temp_dir}/basic.mdx'
        create_mdx(mdx_file_path, remove_db=True)

        builder = IndexBuilder(mdx_file_path)

        records = builder.query('doe')
        self.assertEqual(records, [
            'a deer, a female deer.'
        ])

        self.assertEqual(builder.headers['Title'], 'Example Dictionary')

        builder.index_manager.db.close()

    def test_rebuild(self):
        builder = IndexBuilder(self.mdx_file_path)
        builder.rebuild()

        builder.index_manager.db.close()
    
    def test_build_mdd_index(self):
        mdd_file_path = f'{temp_dir}/basic.mdd'
        create_mdd(mdd_file_path, remove_db=True)

        builder = IndexBuilder(mdd_file_path)
        builder.index_manager.db.close()

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

    def test_process_link_record(self):
        self.builder = IndexBuilder(self.mdx_file_path)
        records = self.builder.query('口内')
        self.assertEqual(records, [
            '嘴裡。'
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

        os.remove(self.mdx_file_path)
        if os.path.exists(self.db_file_path):
            os.remove(self.db_file_path)


if __name__ == '__main__':
    unittest.main()