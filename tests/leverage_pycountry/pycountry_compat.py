import pycountry

num_cnt = len(pycountry.countries)
print(f"{str(type(num_cnt)), num_cnt}")
# 249

itm_one = list(pycountry.countries)[1]
print(f"{str(type(itm_one)), itm_one}")
# Country(alpha_2='AF', alpha_3='AFG', name='Afghanistan', numeric='004', official_name='Islamic Republic of Afghanistan')

# germany = pycountry.countries.get(alpha_2='DE')
# germany
# Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276', official_name='Federal Republic of Germany')
# germany.alpha_2
# 'DE'
# germany.alpha_3
# 'DEU'
# germany.numeric
# '276'
# germany.name
# 'Germany'
# germany.official_name
# 'Federal Republic of Germany'
