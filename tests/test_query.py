import unittest
import os

from setup import temp_dir, mocks_dir
from mocks import create_mdx
from mdict_query_r.query import Querier, Dictionary, Record
from mdict_query_r.mdict import Entry

class TestQuery(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_query(self):
        mdx_file_path = f'{mocks_dir}/test_querier.mdx'
        create_mdx(mdx_file_path)
        querier = Querier([Dictionary('test', mdx_file_path)])
        records = querier.query('doe')
        self.assertEqual(records, [
            Record(
                dictionary_name='test', 
                entry=Entry(
                    id=1, 
                    key_text='doe',
                    data='a deer, a female deer.'
                )
            )
        ])
    
    @unittest.skip('local test')
    def test_init_multi_dicts(self):
        names = [
            '新時代日漢辭典',
            'プログレッシブ和英中辞典_v4',
            '三合一日文詞典'
        ]

        for n in names:
            db_filepath = f'{temp_dir}/{n}.mdx.db'
            if os.path.exists(db_filepath):
                os.remove(db_filepath)
            
        dictionaries = map(
            lambda x: Dictionary(x, f'{temp_dir}/{x}.mdx'),
            names
        )
        querier = Querier(dictionaries)

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
            Record(
                dictionary_name='新時代日漢辭典', 
                entry=Entry(
                    id=126843, 
                    key_text='青春', 
                    data='<div style="margin-left:0.2em;margin-bottom:5px;"><span style="color:green;font-weight:bold;font-size:1.1em;">せいしゅん</span> <span style="color:purple">⓪</span><span style="color:green;font-size:1.1em;">【青春】</span></div>\r\n<div style="margin-left:1em"><b>1</b><span style="color:purple"> 名 </span>青春。</div>\r\n<div class="sec ex" style="margin-left:3em;color:gray">▸ ～の血をわかす / 青春的熱血沸騰。</div>\r\n<div class="sec ex" style="margin-left:3em;color:gray">▸ ～を謳歌（おうか）する / 歌頌青春。</div>\r\n<div style="margin-left:3em"><span class="sec" style="color:gray;">● ～時代 / 青春時代。</span></div>\r\n<div style="margin-left:1em"><span style="color:purple"><b>衍：</b></span></div>\r\n<div style="margin-left:1em">～き③【～期】〔名〕青春期。</div>\r\n'
                )
            ), 
            Record(
                dictionary_name='プログレッシブ和英中辞典_v4', 
                entry=Entry(
                    id=39685, 
                    key_text='せいしゅん【青春】', 
                    data='<link rel="stylesheet" href="PJE4.css"  type="text/css"/><body><div class="excf"><h3>せいしゅん【青春】</h3><section class="description"><p class="meaning"><i>one\'s</i> youth; youthfulness</p><p class="example"><jpexam>青春の血</jpexam><enexam><i>young</i> blood／the hot blood of <i>youth</i></enexam></p><p class="example"><jpexam>青春の血に燃える</jpexam><enexam>burn with the fire of <i>youth</i></enexam></p><p class="example"><jpexam>彼は青春の情熱を仕事に注いだ</jpexam><enexam>He concentrated on his work with <i>youthful</i> enthusiasm.</enexam></p><p class="subheadword"><em>青春期</em></p><p class="meaning">adolescence</p><p class="subheadword"><em>青春時代</em></p><p class="example"><jpexam>青春時代に</jpexam><enexam>in <i>one\'s</i> youth [young days]</enexam></p></section></div></body>\r\n'
                )
            )
        ])
        

if __name__ == '__main__':
    unittest.main()