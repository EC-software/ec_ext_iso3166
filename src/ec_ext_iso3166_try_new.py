import pprint
import ec_ext_iso3166

""" A New Try
After having consideres things one more time.
What queations (functions) do we really want to ansver here ...

Now the default object is the collection, that we can ask questions.
"""


print(" ------ Welcome to test -------------")

trs = ec_ext_iso3166.Territories()  # Note this returns the entire collection of countries (territories)
print(f"trs: {trs}")

ter_dk = trs.get('DK')  # Get a specific territory by primary key
print(ter_dk)

ter_gl = trs.guess('Nuuk')  # Never return multiple hits (that would not be a guess)

ter_nl = trs.locate('')  # First and foremost, tries to be compatible with https://pypi.org/project/pycountry/

lst_ters1 = trs.find('Rom')  # Allow for multiple returns. Romanina, Italy, ?
lst_ters2 = trs.find('Rome', ['capital'])  # and. Allow search to target specific keys, e.g. 'capital' = 'Rome'
lst_ters2 = trs.find('Ro', ['capital', 'tld'])  # Italy, Romania
lst_ters3 = trs.find(['Ro', 'Pa'], ['capital'])  # Italy, France


# print(terr.get('name_eng'))
# pprint.pprint(terr.get_all())
# val = 'Rom'
# print("=== lookup ===")
# pprint.pprint(terr.lookup(val))
# print("=== guess ===")
# terr.guess(val)
# pprint.pprint(terr.get_all())
# print("=== key ===")

# pprint.pprint(terr.find_all_by_key('mid', val, False))
# pprint.pprint(terr.find_all_by_key('numeric_3', val, False))
