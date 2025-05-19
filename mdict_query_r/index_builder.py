import os
import re
from dataclasses import asdict

from .mdict import MDX, MDD, Entry
from .db_manager import IndexManger

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
        self.link_pattern = r'^@@@LINK='

        if not index_exists:
            self._build()

    def _build(self):
        indexes = self.mdict.get_indexes()

        self.index_manager.insert_indexes([
            asdict(x) for x in indexes
        ])
        
        self.index_manager.insert_headers(self.mdict.header.items())
        self.headers = self._get_hearders()

    def _get_hearders(self):
        headers = {}
        for key, value in self.mdict.header.items():
            str_key = key.decode('utf-8') if isinstance(key, bytes) else key
            str_value = value.decode('utf-8') if isinstance(value, bytes) else value
            headers[str_key] = str_value

        return headers

    def rebuild(self):
        self.index_manager.rebuild()
        self._build()

    def query(self, keyword='', keywords: list[str]=[], ignore_case=False) -> list[Entry]:
        assert(keyword != "" or len(keywords) != 0)

        matched: list[str] = []

        def _query(_keyword='', _keywords: list[str]=[]):

            if ignore_case:
                _keyword = _keyword.lower()
                _keywords = [k.lower() for k in _keywords]

            indexes = self.index_manager.lookup_indexes(_keyword, _keywords)

            data = self.mdict.get_data_by_indexes(indexes)
            if self.mdict_type == 'MDD':
                return data
            
            result: list[Entry] = []
            links = []
        
            for item in data:
                if re.match(self.link_pattern, item.data):
                    key_text = re.sub(self.link_pattern, '', item.data).strip()
                    if key_text not in matched:
                        links.append(key_text)
                else:
                    matched.append(item.key_text)
                    result.append(item)

            if len(links) == 0:
                return result
        
            link_result = _query(_keywords=links)

            return result + link_result
        
        return _query(keyword, keywords)
        