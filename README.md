# MDict Query R

This project is based on [mdict-query](https://github.com/mmjang/mdict-query), [mdict-analysis](https://bitbucket.org/xwang/mdict-analysis/src/master/), [writemdict](https://github.com/zhansliu/writemdict).

You can use this library to query MDX and MDD files. The library will create SQLite files to save dictionary indexes when you initiate a querier or add new dictionaries.

You can also use the original library to query and write MDX and MDD files.

# Install

```bash
pip install mdict_query_r
```

# Usage

## Basic Usage

```python
from mdict_query_r.query import Querier, Dictionary

d = Dictionary('test', 'test.mdx')
querier = Querier([Dictionary('test', mdx_file_path)])
records = querier.query('doe')

# records = [
#     Record(
#         dictionary_name='test',
#         entry=Entry(
#             id=1,
#             key_text='doe',
#             data='a deer, a female deer.'
#         )
#     )
# ]


# query multi words
records = querier.query(keywords=['doe', 'ray'])

# query with case insensitive
records = querier.query('doe', ignore_case=True)
```

## Use mdict lib

use [readmdict](https://bitbucket.org/xwang/mdict-analysis/src/master/) to directly read mdx file.

```python
from mdict_query_r.lib.readmdict import MDX

mdx = MDX('test.mdx')
```

use [writemdict](https://github.com/zhansliu/writemdict) to directly create mdx file.

```python
from mdict_query_r.lib.writemdict import MDictWriter

dictionary = {
    "doe": "a deer, a female deer.",
    "ray": "a drop of golden sun.",
    "me": "a name I call myself.",
    "far": "a long, long way to run."
}

writer = MDictWriter(
    dictionary,
    title="Example Dictionary",
    description="This is an example dictionary."
)

with open('test.mdx', 'wb') as f:
    writer.write(f)
```
