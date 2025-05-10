from dataclasses import dataclass
import os

from .index_builder import IndexBuilder
from .mdict import Entry

@dataclass
class Dictionary:
    name: str
    filepath: str
    _db: IndexBuilder = None

@dataclass
class Record:
    dictionary_name: str
    entry: Entry
    
class Querier:

    def __init__(self, dictionaries: list[Dictionary]):
        self._builders: dict[str, Dictionary] = {}
        self.add_dictionaries(dictionaries)

    def add_dictionaries(self, dictionaries: list[Dictionary]):
        for dictionary in dictionaries:
            self.add_dictionary(dictionary)

    def add_dictionary(self, dictionary: Dictionary):
        if dictionary._db == None and os.path.exists(dictionary.filepath):
            dictionary._db = IndexBuilder(dictionary.filepath)
            self._builders[dictionary.filepath] = dictionary

    def query(self, keyword='', keywords: list[str]=[], ignore_case=False):
        records: list[Record] = []

        for item in self._builders.values():
            entries = item._db.query(keyword, keywords, ignore_case)
            if entries:
                for entry in entries:
                    records.append(
                        Record(
                            dictionary_name=item.name,
                            entry=entry
                        )
                    )
        
        return records
