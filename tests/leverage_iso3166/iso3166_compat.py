import iso3166
#import iso3166_ext as iso3166

print("------------- Countries. level ------")
cntrs = iso3166.countries
print(cntrs)
print(dir(cntrs))
print([itm for itm in dir(cntrs) if itm[:1] != '_'])
# print(f"version: {iso3166.__version__}")  # Not found in: https://pypi.org/project/iso3166/
print(f"__doc__: {iso3166.__doc__}")
print(f"__file__: {iso3166.__file__}")
print(f"__name__: {iso3166.__name__}")
print(f"__package__: {iso3166.__package__}")  # seems identical to __name__


print("------------- Countries. level ------")

cnt = cntrs.get('DK')
print(cnt)