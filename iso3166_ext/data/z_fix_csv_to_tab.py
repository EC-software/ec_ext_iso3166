
import os

for root, dirs, files in os.walk("."):
    for name in files:
        if name.endswith('.csv'):
            print(os.path.join(root, name))
            with open(name, 'r') as fil_in:
                lst_lns = fil_in.readlines()
            lst_lns_ou = list()
            for str_in in lst_lns:
                if '#' in str_in[1:]:
                    print(str_in)
                lst_tok = str_in.split('#')
                str_lft = lst_tok[0]
                str_lft = '\t'.join([itm.lstrip() for itm in str_lft.split(',', 1)])  # replace(',', '\t) in the left part
                lst_tok[0] = str_lft
                str_ou = '#'.join(lst_tok)
                lst_lns_ou.append(str_ou)
            with open(name.replace('.csv', '.tab'), 'w') as fil_ou:
                fil_ou.writelines(lst_lns_ou)