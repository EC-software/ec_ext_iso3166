
import ec_ext_iso3166

print(" ------ Velcome to test -------------")

terr = ec_ext_iso3166.Territory('Franc')

#print(terr)
print(terr.keys())
print(terr.get('name_eng'))
print(terr.getall())