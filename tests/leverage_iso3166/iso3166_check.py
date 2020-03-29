
import iso3166

from iso3166 import countries

""" I sort of like this ... """

print(dir(iso3166))

print(countries.get('us'))
# Country(name=u'United States', alpha2='US', alpha3='USA', numeric='840')
print(countries.get('ala'))
# Country(name=u'\xc5land Islands', alpha2='AX', alpha3='ALA', numeric='248')
print(countries.get(8))
# Country(name=u'Albania', alpha2='AL', alpha3='ALB', numeric='008')

for c in countries:
       print(c)

""" Each return a dict, but with a different key """
print(f"by name: {iso3166.countries_by_name}")
print(f"by nmrc: {iso3166.countries_by_numeric}")
print(f"by alp2: {iso3166.countries_by_alpha2}")
print(f"by alp3: {iso3166.countries_by_alpha3}")
