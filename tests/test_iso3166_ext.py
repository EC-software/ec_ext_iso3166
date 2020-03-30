import unittest
import iso3166_ext

class TestIso3166_ext_Territory(unittest.TestCase):
    """ Test the Territory (singular) """

    ter_tst = iso3166_ext.Territory(['alpha_2', 'alpha_3', 'numeric_3', 'name_en'], ['KY', 'CYM', '136', 'Cayman Islands (the)'])

    def test_a(self):
        self.assertIsInstance(self.ter_tst, iso3166_ext.Territory)
        #self.assertDictEqual(..., {'alpha_2': 'KY', 'alpha_3': 'CYM', 'numeric_3': '136', 'name_en': 'Cayman Islands (the)'})

    ter_tst.add_ext_key(['alpha_2', 'some_item'], ['KY', 'some value'])
    print(ter_tst._data)

# class TestIso3166Compability(unittest.TestCase):

    # def test_a(self):
    #     self.assertEqual(len(pycountry.countries), 249)
    #     self.assertEqual(list(pycountry.countries)[1],
    #     [Country(alpha_2='AF', alpha_3='AFG', name='Afghanistan', numeric='004', official_name='Islamic Republic of Afghanistan'])

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()