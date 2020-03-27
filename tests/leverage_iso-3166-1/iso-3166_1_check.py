from iso3166 import Country

print(str(type(Country.kr)), Country.kr)
# <Country.kr>
print(Country.kr.alpha2)
# KR
print(Country.kr.alpha3)
# KOR
print(Country.kr.numeric)
# 410
print(Country.kr.english_short_name)

"""
Everything is an enum? Is that cool?
Only lookup by alpha-2
Literally only a _init_.py :-(
all data storesd in a .csv
alpha-2, alpha-3, numeric-3 and short_english_name. That's it.
"""
import iso3166
print(iso3166)

Can't co-exist with iso3166 since they use same dir name in install_packages

I'm not a fan ...