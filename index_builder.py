import os

from mdict import MDX
from db_manager import MdxIndexManger

class IndexBuilder:

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))
        self.mdx = MDX(filepath)

        _filename, _file_ext = os.path.splitext(filepath)

        index_exists = os.path.isfile(filepath + '.db')
        self.index_manager = MdxIndexManger(filepath)

        if not index_exists:
            indexes = self.mdx.get_indexes()

            for i in range(0, len(indexes), 500):
                self.index_manager.Index.insert_many([
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
                for item in indexes[i:i + 500]
                ]).execute()

            self.index_manager.Header.insert_many(self.mdx.header.items()).execute()
    
    def lookup_indexes(self, keyword='', keywords=[]):
        assert(keyword != "" or len(keywords) != 0)

        if len(keywords) != 0:
            return self.index_manager.Index.select().where(
                self.index_manager.Index.key_text.in_(keywords)
            ).dicts()

        return self.index_manager.Index.select().where(
            self.index_manager.Index.key_text == keyword
        ).dicts()

    def query(self, keyword='', keywords: list[str]=[], ignore_case=False):
        assert(keyword != "" or len(keywords) != 0)

        if ignore_case:
            keyword = keyword.lower()
            keywords = [k.lower() for k in keywords]

        indexes = self.lookup_indexes(keyword, keywords)
        return self.mdx.get_data_by_indexes(indexes)
        