# from iso3166_ext import world
import iso3166_ext

""" A New Try
After having considered things one more time.
What questions (functions) do we really want to answer here ...

Now the default object is the collection, that we can ask questions.
"""

# print(f"Dump: {trs.dump_as_text()}")
# key_a = 'name_eng'
# key_b = 'name_short_en'
# for key_c in trs._data.keys():
#     if all([k in trs._data[key_c].keys() for k in [key_a, key_b]]):
#         if trs._data[key_c][key_a] != trs._data[key_c][key_b]:
#             print(f" - k: {key_c} ({key_a},{key_b}) >> {trs._data[key_c][key_a]} != {trs._data[key_c][key_b]}")

print(" ------ Welcome to tests-bed -------------")
print(f"data root dir: {iso3166_ext.root_dir}")
trs = iso3166_ext.Territories()  # Note this returns the entire collection of countries (territories)
print(f"Done building Territories ...")

# print(f"Sorted categories: {trs.categories()}")
# print(f"Orderd categories: {iso3166_ext.order_iso3166_keys(trs.categories())}")
# print(f"Missing values: {trs.list_missing_values()}")
#
# token = "DK"
# ter_dk = trs.get(token)  # Get a specific territory by primary key
# print(f"What: {str(type(ter_dk))}")
# print(f"get({token}) = {ter_dk.as_text()}")
#
# token = "AQ"
# ter_x = trs.get(token)  # Get a specific territory by primary key
# print(f"get({token}) = {ter_x.as_text()}")

# lst_ters1 = trs.find('Rom')  # Allow for multiple returns. Romanina, Italy, ?
# lst_ters2 = trs.find('Rome', ['capital'])  # and. Allow search to target specific keys, e.g. 'capital' = 'Rome'
# lst_ters2 = trs.find('Ro', ['capital', 'tld'])  # Italy, Romania
# lst_ters3 = trs.find(['Ro', 'Pa'], ['capital'])  # Italy, France
# lst_ters3 = trs.find(['Douglas'], ['capital'])  # multiple?
# lst_ters3 = trs.find(['Brades'], ['capital'])  # has 3 capitols
# tests "French Southern Territories" >> "Saint-Pierre, Réunion"

# ter_gl = trs.guess('Nuuk')  # Never return multiple hits (that would't be a guess)
#
# ter_nl = trs.locate('')  # First and foremost, tries to be compatible with https://pypi.org/project/pycountry/

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
