
import iso3166

from iso3166 import countries

print(countries.get('us'))
# Country(name=u'United States', alpha2='US', alpha3='USA', numeric='840')
print(countries.get('ala'))
# Country(name=u'\xc5land Islands', alpha2='AX', alpha3='ALA', numeric='248')
print(countries.get(8))
# Country(name=u'Albania', alpha2='AL', alpha3='ALB', numeric='008')

