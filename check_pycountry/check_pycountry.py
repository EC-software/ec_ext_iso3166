import pycountry
print(len(pycountry.countries))
print(list(pycountry.countries)[0])

# get
germany = pycountry.countries.get(alpha_2='DE')
print(germany)
print(germany.alpha_2)
print(germany.alpha_3)
print(germany.numeric)
print(germany.name)
print(germany.official_name)

# search_fuzzy
print(pycountry.countries.search_fuzzy('England'))
print(pycountry.countries.search_fuzzy('Cote'))

# lookup
print(pycountry.countries.lookup('de'))

print()
print()