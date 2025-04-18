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

    @unittest.skip('local test')
    def test_query_multi_dicts(self):
        mdx_file_path1 = f'{temp_dir}/新時代日漢辭典.mdx'
        mdx_file_path2 = f'{temp_dir}/プログレッシブ和英中辞典_v4.mdx'
        querier = Querier([
            Dictionary('新時代日漢辭典', mdx_file_path1),
            Dictionary('プログレッシブ和英中辞典_v4', mdx_file_path2)
            ])
        records = querier.query('青春')
        self.assertEqual(records, [
            {
                'dictionary': '新時代日漢辭典', 
                'record': '<div style="margin-left:0.2em;margin-bottom:5px;"><span style="color:green;font-weight:bold;font-size:1.1em;">せいしゅん</span> <span style="color:purple">⓪</span><span style="color:green;font-size:1.1em;">【青春】</span></div>\r\n<div style="margin-left:1em"><b>1</b><span style="color:purple"> 名 </span>青春。</div>\r\n<div class="sec ex" style="margin-left:3em;color:gray">▸ ～の血をわかす / 青春的熱血沸騰。</div>\r\n<div class="sec ex" style="margin-left:3em;color:gray">▸ ～を謳歌（おうか）する / 歌頌青春。</div>\r\n<div style="margin-left:3em"><span class="sec" style="color:gray;">● ～時代 / 青春時代。</span></div>\r\n<div style="margin-left:1em"><span style="color:purple"><b>衍：</b></span></div>\r\n<div style="margin-left:1em">～き③【～期】〔名〕青春期。</div>\r\n'
            }, 
            {
                'dictionary': 'プログレッシブ和英中辞典_v4', 
                'record': '@@@LINK=せいしゅん【青春】\r\n'
            }
        ])

        

if __name__ == '__main__':
    unittest.main()