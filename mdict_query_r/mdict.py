# extend basic MDX

from struct import pack, unpack
from dataclasses import dataclass
from typing import Any

# zlib compression is used for engine version >=2.0
import zlib
# LZO compression is used for engine version < 2.0
from .lib import lzo

from .lib.readmdict import MDX as _MDX, MDD as _MDD, MDict
from .db_manager import Index

@dataclass
class MdictIndex:
    # 关键词
    key_text: str
    # record_block 开始的位置
    file_pos: int
    # record_block 压缩前的大小
    compressed_size: int
    # 解压后的大小
    decompressed_size: int
    # record_block 的压缩类型
    record_block_type: int
    # record_start，record_end，offset 
    # 用于从 record_block 中提取某一调记录
    record_start: int
    record_end: int
    offset: int

@dataclass
class Entry:
    id: int
    key_text: str
    data: Any

def _get_indexes(mdict: MDict):
    check_block = False

    with open(mdict._fname, 'rb') as f:
        f.seek(mdict._record_block_offset)

        num_record_blocks = mdict._read_number(f)
        num_entries = mdict._read_number(f)
        assert(num_entries == mdict._num_entries)
        record_block_info_size = mdict._read_number(f)
        record_block_size = mdict._read_number(f)
        
        record_block_info_list = []
        size_counter = 0

        for i in range(num_record_blocks):
            compressed_size = mdict._read_number(f)
            decompressed_size = mdict._read_number(f)
            record_block_info_list.append(
                (compressed_size, decompressed_size)
            )
            size_counter += mdict._number_width * 2
        assert(size_counter == record_block_info_size)

        result: list[MdictIndex] = []
        # actual record block data
        offset = 0
        i = 0
        size_counter = 0
        for compressed_size, decompressed_size in record_block_info_list:
            current_pos = f.tell()
            record_block_compressed = f.read(compressed_size)
            ###### 要得到 record_block_compressed 需要得到 compressed_size (这个可以直接记录）
            ###### 另外还需要记录当前 f 对象的位置
            ###### 使用 f.tell() 命令/ 在建立索引是需要 f.seek()
            # 4 bytes indicates block compression type
            record_block_type = record_block_compressed[:4]
            # 4 bytes adler checksum of uncompressed content
            adler32 = unpack('>I', record_block_compressed[4:8])[0]
            # no compression
            if record_block_type == b'\x00\x00\x00\x00':
                _type = 0
                record_block = record_block_compressed[8:]
            # lzo compression
            elif record_block_type == b'\x01\x00\x00\x00':
                _type = 1
                if lzo is None:
                    print("LZO compression is not supported")
                    break
                # decompress
                header = b'\xf0' + pack('>I', decompressed_size)
                if check_block:
                    record_block = lzo.decompress(record_block_compressed[8:], initSize = decompressed_size, blockSize=1308672)
            # zlib compression
            elif record_block_type == b'\x02\x00\x00\x00':
                # decompress
                _type = 2
                if check_block:
                    record_block = zlib.decompress(record_block_compressed[8:])
            ###### 这里比较重要的是先要得到 record_block, 而 record_block 是解压得到的，其中一共有三种解压方法
            ###### 需要的信息有 record_block_compressed, decompress_size,
            ###### record_block_type
            ###### 另外还需要校验信息 adler32
            # notice that adler32 return signed value
            if check_block:
                assert(adler32 == zlib.adler32(record_block) & 0xffffffff)
                assert(len(record_block) == decompressed_size)
            # split record block according to the offset info from key block
            while i < len(mdict._key_list):
                ### 用来保存索引信息的空字典
                record_start, key_text = mdict._key_list[i]
                index = MdictIndex(
                    key_text = key_text.decode('utf-8'),
                    file_pos = current_pos,
                    compressed_size = compressed_size,
                    decompressed_size = decompressed_size,
                    record_block_type = _type,
                    record_start = record_start,
                    record_end = 0,
                    offset = offset,
                )

                # reach the end of current record block
                if record_start - offset >= decompressed_size: 
                    break
                # record end index
                if i < len(mdict._key_list) - 1:
                    record_end = mdict._key_list[i + 1][0]
                else:
                    record_end = decompressed_size + offset
                index.record_end = record_end
                i += 1

                result.append(index)

            offset += decompressed_size 
            size_counter += compressed_size

        return result

def _get_data_by_indexes(mdict: MDict, indexes: list[Index], encoding=None):
    with open(mdict._fname, 'rb') as f:
        result: list[Entry] = []
        
        for index in indexes:
            f.seek(index.file_pos)
            record_block_compressed = f.read(index.compressed_size)
            record_block_type = record_block_compressed[:4]
            record_block_type = index.record_block_type
            decompressed_size = index.decompressed_size

            #adler32 = unpack('>I', record_block_compressed[4:8])[0]
            if record_block_type == 0:
                _record_block = record_block_compressed[8:]
                # lzo compression
            elif record_block_type == 1:
                header = b'\xf0' + pack('>I', index.decompressed_size)
                _record_block = lzo.decompress(record_block_compressed[8:], initSize = decompressed_size, blockSize=1308672)
                    # zlib compression
            elif record_block_type == 2:
                # decompress
                _record_block = zlib.decompress(record_block_compressed[8:])
            data = _record_block[index.record_start - index.offset:index.record_end - index.offset]

            if encoding != None:
                data = data.decode(encoding, errors='ignore').strip(u'\x00')

            result.append(Entry(id=index.id, key_text=index.key_text, data=data))

        return result

class MDX(_MDX):

    def get_indexes(self):
        return _get_indexes(self)
        
    def get_data_by_indexes(self, indexes: list[Index]):
        encoding = self.header[b'Encoding'].decode('utf-8')
        return _get_data_by_indexes(self, indexes, encoding=encoding)
        
class MDD(_MDD):

    # this is same with MDX.get_index
    def get_indexes(self):
        return _get_indexes(self)
    
    def get_data_by_indexes(self, indexes: list[Index]):
        return _get_data_by_indexes(self, indexes)