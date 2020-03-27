import sys
str_ffn_in = r"/home/martin/PycharmProjects/ec_ext_iso3166/data/iso3166.table"
str_ffn_ou = r"/home/martin/PycharmProjects/ec_ext_iso3166/ext_iso3166/iso3166_tmp.csv"

if __name__ == '__main__':

    with open(str_ffn_ou, 'w') as fil_ou:
        with open(str_ffn_in, 'r') as fil_in:
            lst_lines = fil_in.readlines()
            print(lst_lines)
            lst_lines = [tok.strip() for tok in lst_lines]  # strip all lines
            print(lst_lines)
            for n in range(0, 2250, 9):
                english = lst_lines[n]
                french = lst_lines[n+2]
                alpha_2 = lst_lines[n+4]
                alpha_3 = lst_lines[n+6]
                numeric = lst_lines[n+8]
                str_ou ="{}, {}, {}, {}, {}".format(alpha_2, alpha_3, numeric, english, french)
                fil_ou.write(str_ou+'\n')
                print(str_ou)
            sys.exit(999)