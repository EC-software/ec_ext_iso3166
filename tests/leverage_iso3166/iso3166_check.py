
import iso3166
from iso3166 import countries

"""
I sort of like this ... 
https://pypi.org/project/iso3166/
pip install iso3166
"""

for itm in sorted(dir(iso3166)):
       print(f" - {itm}")

# From the online example usage (slightly modified) : -------------------------

print(countries.get('us'))
# Country(name=u'United States', alpha2='US', alpha3='USA', numeric='840')
print(countries.get('ala'))
# Country(name=u'\xc5land Islands', alpha2='AX', alpha3='ALA', numeric='248')
print(countries.get(8))
# Country(name=u'Albania', alpha2='AL', alpha3='ALB', numeric='008')

print("------")
for c in countries:
       pass#print(c)
print("------")

""" Each return a dict, but with a different key """
print(f"by name: {iso3166.countries_by_name}")
print(f"by nmrc: {iso3166.countries_by_numeric}")
print(f"by alp2: {iso3166.countries_by_alpha2}")
print(f"by alp3: {iso3166.countries_by_alpha3}")

# End of online example usage: ------------------------------------------------

# More investigative...
print("\n============= More investigative ... ==========================================")
print("------------- Country. level ------")
obj = iso3166.countries.get('us')   # <------------------------- I don't like this overwrite of .get, but
print(obj)
print(str(type(obj)))
print([itm for itm in dir(obj) if itm[:2] != '__'])

# Dig into USA
print('alpha2:', obj.alpha2)
print('alpha3:', obj.alpha3)
print('numeric:', obj.numeric)
print('name:', obj.name)
print('apolitical_name:', obj.apolitical_name)
print('count:', obj.count('United States of America'))
print('count:', obj.count('840'))
print('count:', obj.count('non-sense'))
print('index:', obj.index('USA'))
print('obj[2]:', obj[2])

# All the same for Denmark
obj = iso3166.countries.get('dk')
print('alpha2:', obj.alpha2)
print('alpha3:', obj.alpha3)
print('numeric:', obj.numeric)
print('name:', obj.name)
print('apolitical_name:', obj.apolitical_name)
print('count:', obj.count('United States of America'))
print('count:', obj.count('840'))
print('count:', obj.count('non-sense'))
# print('index:', obj.index('USA')) -- this crashes ...
print('obj[2]:', obj[2])


print("------------- Countries. level ------")
obj = iso3166.countries
print(obj)
print(str(type(obj)))
# print(dir(obj))
print([itm for itm in dir(obj) if itm[:2] != '__'])