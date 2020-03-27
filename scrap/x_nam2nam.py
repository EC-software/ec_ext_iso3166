
str_ffn_in1 = r"/home/martin/PycharmProjects/ec_ext_iso3166/data/mid_codes.txt"
str_ffn_in2 = r"/home/martin/PycharmProjects/ec_ext_iso3166/ext_iso3166/iso3166-1.csv"

if __name__ == '__main__':

    lst_ref = list()
    with open(str_ffn_in2, 'r') as fil_i2:
        for line in fil_i2:
            if ',' in line:
                lst_in2 = [tok.strip() for tok in line.split(',')]
                if len(lst_in2) == 5 and len(lst_in2[0]) == 2:
                    lst_ref.append([lst_in2[0], lst_in2[3]])

    with open(str_ffn_in1, 'r') as fil_i1:
        for line in fil_i1:
            al2 = None
            mid, cnm = [tok.replace('"','').replace(',','').strip() for tok in line.split(':')]
            cnm1 = cnm.split(' ')[0]
            #print(mid, cnm1)
            for ref in lst_ref:
                ##print("ref:", ref)
                if ref[1].find(cnm1) > -1:
                    al2 = ref[0]
            if al2:
                print("{}, {}".format(al2, mid))
            else:
                print(cnm, mid)