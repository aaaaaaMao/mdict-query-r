import os

from peewee import *

class IndexManger():

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))

        _, ext = os.path.splitext(filepath)
        
        db_filepath = filepath
        if ext != '.db':
            db_filepath += '.db'

        self.db = SqliteDatabase(db_filepath)
        
        self.db.connect()
        tables = [self.Header, self.Index]
        self.db.bind(tables)
        self.db.create_tables(tables)

    class Index(Model):
        class Meta:
            table_name = 'mdict_indexes'
        
        key_text = TextField(null=False)
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