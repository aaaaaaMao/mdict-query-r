import os

from peewee import *

class MdxIndexManger():

    def __init__(self, filepath: str):
        assert(os.path.isfile(filepath))
        self.db = SqliteDatabase(filepath + '.db')
        
        self.db.connect()
        tables = [self.Index, self.Header]
        self.db.bind(tables)
        self.db.create_tables(tables)

    class Index(Model):
        class Meta:
            table_name = 'mdx_index'
        
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
            tabel_name = 'mdx_header'
        
        key = TextField(null=False)
        value = TextField()