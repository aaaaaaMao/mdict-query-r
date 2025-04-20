import unittest

from setup import mocks_dir
from mdict_query_r.lib.writemdict import MDictWriter
from mdict_query_r.lib.readmdict import MDX, MDD

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

        filepath = f'{mocks_dir}/basic.mdx'
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

    def test_creare_mdd(self):
        # A raw PNG file, with size 10x10, all red.
        raw_image = (b"\x89PNG\r\n\x1a\n"
                    b"\0\0\0\x0dIHDR"
                    b"\0\0\0\x0a\0\0\0\x0a\x08\x02\x00\x00\x00"
                    b"\x02\x50\x58\xea"
                    b"\x00\x00\x00\x12IDAT"
                    b"\x18\xd3\x63\xfc\xcf\x80\x0f\x30\x31\x8c\x4a\x63\x01\x00\x41\x2c\x01\x13"
                    b"\x65\x62\x10\x33"
                    b"\0\0\0\0IEND"
                    b"\xae\x42\x60\x82")
        
        filepath = f'{mocks_dir}/basic_mdd.mdd'
        with open(filepath, 'wb') as f:
            d_mdd = {"\\red.png": raw_image}
            writer = MDictWriter(d_mdd, "Dictionary with MDD file", "This dictionary tests MDD file handling.", is_mdd=True)
            writer.write(f)

        mdd = MDD(filepath)
        self.assertEqual(len(mdd), 1)

    
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()