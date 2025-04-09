import os
from dataclasses import asdict

from mdict import MDX, MDD
from db_manager import IndexManger

class IndexBuilder:

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))
        _, _file_ext = os.path.splitext(filepath)
        assert(_file_ext in ['.mdx', '.mdd'])

        if _file_ext == '.mdx':
            self.mdict_type = 'MDX'
            self.mdict = MDX(filepath)
        else:
            self.mdict_type = 'MDD'
            self.mdict = MDD(filepath)

        index_exists = os.path.isfile(filepath + '.db')
        self.index_manager = IndexManger(filepath)

        if not index_exists:
            self._build()

    def _build(self):
        indexes = self.mdict.get_indexes()

        batch = 2000
        for i in range(0, len(indexes), batch):
            self.index_manager.Index.insert_many([
              asdict(x) for x in indexes[i:i + batch]
            ]).execute()

        self.index_manager.Header.insert_many(self.mdict.header.items()).execute()
    
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
        return self.mdict.get_data_by_indexes(indexes)
        