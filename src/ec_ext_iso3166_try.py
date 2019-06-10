import pprint
import ec_ext_iso3166

print(" ------ Velcome to test -------------")

terr = ec_ext_iso3166.Territory('Rom')

#print(terr)
#print(terr.keys())
print(terr.get('name_eng'))
pprint.pprint(terr.get_all())
val = 'Rom'
print("=== lookup ===")
pprint.pprint(terr.lookup(val))
print("=== guess ===")
terr.guess(val)
pprint.pprint(terr.get_all())
print("=== key ===")
# pprint.pprint(terr.find_all_by_key('mid', val, False))
# pprint.pprint(terr.find_all_by_key('numeric_3', val, False))
