
import ec_ext_iso3166

terr = ec_ext_iso3166.Territory('DK')

print(terr)
print(terr.keys())
print(terr.get('name_eng'))
print(terr.getall())