import sys

str_ffn_in = r"/home/martin/PycharmProjects/ec_ext_iso3166/data/tld_org.csv"
str_ffn_ou = r"/home/martin/PycharmProjects/ec_ext_iso3166/src/tld.csv"

if __name__ == '__main__':

    with open(str_ffn_ou, 'w') as fil_ou:
        with open(str_ffn_in, 'r') as fil_in:
            for line in fil_in:
                data, comm = None, None
                tld = None
                if "#" in line:
                    data, comm = [tok.strip() for tok in line.split('#', 1)]
                else:
                    data, comm = line.strip(), None
                if '\t' in data:
                    lst_lin = [tok.strip() for tok in data.split('\t')]
                    al2 = lst_lin[0]
                    tld = lst_lin[3]
                    str_ou = "{}, {}".format(al2, tld)
                    if not al2.lower() == tld.lstrip('.').lower():
                        print("DIFF:", str_ou)
                    fil_ou.write(str_ou)
                else:
                    pass#print("ERR 1 - not TAB: {}".format(data))
                if comm:
                    fil_ou.write(" # {}\n".format(comm))
                else:
                    fil_ou.write("\n".format(comm))
