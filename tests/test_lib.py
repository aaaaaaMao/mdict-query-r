import os
import unittest

from setup import temp_dir
from lib.writemdict import MDictWriter
from lib.readmdict import MDX

class TestLib(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_basic_write(self):
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

        filepath = f'{temp_dir}/basic.mdx'
        with open(filepath, 'wb') as f:
            writer.write(f)

        mdx = MDX(filepath)
        self.assertEqual(len(mdx), 4)
        self.assertEqual(
            mdx.header.get(b"Title"),
            b"Example Dictionary"
        )
        self.assertEqual(
            mdx.header.get(b"Description"),
            b"This is an example dictionary."
        )

    
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()