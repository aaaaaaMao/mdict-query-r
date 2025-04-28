from dataclasses import dataclass
import os
from typing import Any

from .index_builder import IndexBuilder

@dataclass
class Dictionary:
    name: str
    filepath: str

class Querier:

    def __init__(self, dictionaries: list[Dictionary]):
        self._builders: dict[str, dict[str, Any]] = {}
        self.add_dictionaries(dictionaries)

    def add_dictionaries(self, dictionaries: list[Dictionary]):
        for dictionary in dictionaries:
            self.add_dictionary(dictionary)

    def add_dictionary(self, dictionary: Dictionary):
        if os.path.exists(dictionary.filepath):
            self._builders[dictionary.filepath] = {
                'name': dictionary.name,
                'builder': IndexBuilder(dictionary.filepath)
            }

    def query(self, keyword='', keywords: list[str]=[], ignore_case=False):
        result = []

        for item in self._builders.values():
            records = item['builder'].query(keyword, keywords, ignore_case)
            if records:
                for r in records:
                    result.append({
                        'dictionary': item['name'],
                        'record': r
                    })
        
        return result
