import os
import pathlib
import unittest

class TestStringMethods(unittest.TestCase):


    def test_get_directoty_from_path(self):
        path = ".pdf/test/AF_Dealer_Pricelist_072020_w.pdf"
        # print(pathlib.Path(path).parent.resolve()))
        self.assertEqual(".pdf\\test",str(pathlib.Path(path).parent.resolve()))
        
    def test_get_filename_from_path(self):
        path = ".pdf/test/AF_Dealer_Pricelist_072020_w.pdf"
        print(str(os.path.basename(path)))
        self.assertEqual("AF_Dealer_Pricelist_072020_w.pdf",str(os.path.basename(path)))
        

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
