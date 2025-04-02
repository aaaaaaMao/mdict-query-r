import os

from mdict import MDX
from db_manager import MdxIndexManger

class IndexBuilder:

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))

        _filename, _file_ext = os.path.splitext(filepath)

        index_exists = os.path.isfile(filepath + '.db')
        index_manager = MdxIndexManger(filepath)

        if not index_exists:
            mdx = MDX(filepath)
            result = mdx.get_index()
            print(len(mdx), 1, len(result['index_dict_list']))
            data = result['index_dict_list']
            # for i in range(0, len(data), 500):
            #     index_manager.Index.insert_many([
            #     (
            #         item['key_text'],
            #             item['file_pos'],
            #             item['compressed_size'],
            #             item['decompressed_size'],
            #             item['record_block_type'],
            #             item['record_start'],
            #             item['record_end'],
            #             item['offset']
            #     )
            #     for item in data[i:i + 500]
            #     ]).execute()

            index_manager.Header.insert_many(mdx.header.items()).execute()