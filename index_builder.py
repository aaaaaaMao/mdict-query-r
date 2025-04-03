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
            index = mdx.get_index()

            for i in range(0, len(index), 500):
                index_manager.Index.insert_many([
                (
                    item['key_text'],
                        item['file_pos'],
                        item['compressed_size'],
                        item['decompressed_size'],
                        item['record_block_type'],
                        item['record_start'],
                        item['record_end'],
                        item['offset']
                )
                for item in index[i:i + 500]
                ]).execute()

            index_manager.Header.insert_many(mdx.header.items()).execute()