import pprint
import ec_ext_iso3166

print(" ------ Velcome to test -------------")

terr = ec_ext_iso3166.Territory('vietnam')

#print(terr)
#print(terr.keys())
print(terr.get('name_eng'))
pprint.pprint(terr.get_all())
val = '208'
print("=== all ===")
pprint.pprint(terr.find_all_in_any(val, False))
print("=== key ===")
pprint.pprint(terr.find_all_by_key('mid', val, False))
pprint.pprint(terr.find_all_by_key('numeric_3', val, False))
