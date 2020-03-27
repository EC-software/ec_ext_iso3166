import unittest
import pycountry

# germany = pycountry.countries.get(alpha_2='DE')
# germany
# Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276', official_name='Federal Republic of Germany')
# germany.alpha_2
# 'DE'
# germany.alpha_3
# 'DEU'
# germany.numeric
# '276'
# germany.name
# 'Germany'
# germany.official_name
# 'Federal Republic of Germany'


class TestPyCountryMethods(unittest.TestCase):

    def test_a(self):
        self.assertEqual(len(pycountry.countries), 249)
        self.assertEqual(list(pycountry.countries)[1],
        [Country(alpha_2='AF', alpha_3='AFG', name='Afghanistan', numeric='004', official_name='Islamic Republic of Afghanistan'])

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