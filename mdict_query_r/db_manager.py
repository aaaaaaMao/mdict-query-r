import os

from peewee import *

class Index(Model):
    class Meta:
        table_name = 'mdict_indexes'

    id = AutoField()
    key_text = TextField(null=False, index=True)
    file_pos = IntegerField()
    compressed_size = IntegerField()
    decompressed_size = IntegerField()
    record_block_type = IntegerField()
    record_start = IntegerField()
    record_end = IntegerField()
    offset = IntegerField()

class Header(Model):
    class Meta:
        table_name = 'mdict_headers'
    
    key = TextField(null=False)
    value = TextField()


class IndexManger():

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))

        _, ext = os.path.splitext(filepath)
        
        self.db_filepath = filepath
        if ext != '.db':
            self.db_filepath += '.db'

        self.db = None
        self.tables = [Header, Index]
        self._build()

    def _build(self):
        assert(self.db == None or self.db.is_closed())
        
        self.db = SqliteDatabase(self.db_filepath)
        
        with self.db.bind_ctx(self.tables):
            self.db.create_tables(self.tables)

    def rebuild(self):
        self.db.close()

        if os.path.exists(self.db_filepath):
            os.remove(self.db_filepath)
        
        self._build()

    def insert_indexes(self, indexes: list):
        batch = 2000
        with self.db.bind_ctx(self.tables):
            for i in range(0, len(indexes), batch):
                Index.insert_many(indexes[i:i + batch]).execute()

    def insert_headers(self, items: list):
        with self.db.bind_ctx(self.tables):
            Header.insert_many(items).execute()

    def lookup_indexes(self, keyword='', keywords: list[str]=[]) -> list[Index]:
        assert(keyword != "" or len(keywords) != 0)

        with self.db.bind_ctx(self.tables):
            if len(keywords) != 0:
                return Index.select().where(
                    Index.key_text.in_(keywords)
                )

            return Index.select().where(
                Index.key_text == keyword
            )