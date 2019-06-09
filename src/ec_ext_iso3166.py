import os

""" EC Extendable ISO 3166 class
The basic official ISO 3166 contains 5 fields for each country:
Numeric, Alpha_2, Alpha_3, English_name and French_name
These are all stored in the default iso3166,csv file.

It's easy to extend this with other fields,
e.g. the countries TLD. Se the tld.csv file for details.
This makes the TLD a fully integrated attribute on each country.

You can easily make your own extensions, by writing new .csv files,
only make sure the 1'st column is an ID that is all ready known, e.g. Alpha-3
"""


class Territory(object):

    """ A Territory.
    Typically a country, but can be independent territories
    or subdivision of countries territories. """


    def add_ext_key(dic_in, lst_hdr, lst_new):
        """ lst_hdr and the keys and lst_new are the values.
        In the dic_iso3166, find the entry with key_on == val_on.
        Add to this entry a new key key_new, with value val_new.
        If key_new all-ready exist, make it a list and append the new value.
        If no entry with key_on == val_on, do nothing. """
        key_on = lst_hdr[0].strip()
        val_on = lst_new[0].strip()
        key_in = lst_hdr[1].strip()
        val_in = lst_new[1].strip()
        if all([len(tok) > 0 for tok in [key_on, val_on, key_in, val_in]]):
            ##print("Add_kv({}:{}) on ({}:{})".format(key_in, val_in, key_on, val_on))
            for key_te in dic_in.keys():  # Loop the Territories
                for key_old in dic_in[key_te].keys():
                    if key_old == key_on:
                        if dic_in[key_te][key_old] == val_on:  # This is the territorry to update
                            terr_upd = dic_in[key_te]
                            ##print(val_on, ">", terr_upd)
                            if key_in in terr_upd.keys():  # The 'new' key all-ready exists
                                if isinstance(terr_upd[key_in], list):  # It's all-reasdy a list, append.
                                    if not val_in in terr_upd[key_in]:
                                        terr_upd[key_in].append(val_in)
                                else:  # If value is new, make a list
                                    if val_in != terr_upd[key_in]:
                                        terr_upd[key_in] = [terr_upd[key_in], val_in]
                            else:
                                terr_upd[key_in] = val_in
                            dic_in[key_te] = terr_upd  # Put the updated territorry back
                            break  # We can't continue the loop, as we have changed dic_in
        return dic_in


    # Read in the basic ISO 3166-1 data from the .csv file
    str_fn_iso3166 = r"iso3166.csv"  # file name for the basic ISO 3166 file
    sep = ','  # assumed separator in this file
    dic_iso3166 = dict()
    with open(str_fn_iso3166, 'r') as fil_iso3166:
        num_cnt = 0
        for line in fil_iso3166:
            #print(line)
            line = line.split('#')[0].strip()  # Skip all comments, and spaces
            if len(line) > 0:
                lst_in = [tok.strip() for tok in line.split(sep)]
                if num_cnt == 0:  # Assumed to be the header
                    lst_head = lst_in
                else:
                    str_num = lst_in[0]  # Note: We assume the first colunm to be the Alpha-2 id.
                    dic_iso3166[str_num] = dict()
                    for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogenious search for all parameters
                        dic_iso3166[str_num][lst_head[n]] = lst_in[n]
                num_cnt += 1
        str_root_path = os.path.realpath(fil_iso3166.name).rsplit(os.sep, 1)[0]+os.sep  # Use this place to look for other .csv files later

    # Read the additional .csv files. NOTE: This is where the EC Extandable comes from !!!
    #print(str_root_path)
    for root, dirs, files in os.walk(str_root_path):
        for name in files:
            if '.csv' in name and not 'iso3166.csv' in name:  # We all ready handled iso3166.csv above
                ##print(os.path.join(root, name))
                num_cnt = 0
                with open(os.path.join(root, name), 'r') as fil_ex:
                    for line in fil_ex:
                        data = line.split('#', 1)[0]
                        if ',' in data:
                            lst_in = [tok.strip() for tok in data.split(',')]
                            if num_cnt == 0:  # Header line
                                lst_head = lst_in
                            else:
                                dic_iso3166 = add_ext_key(dic_iso3166, lst_head, lst_in)
                            num_cnt += 1

    #print(dic_iso3166)



    def __init__(self, clue="", safe=True):
        self.data = dict()
        self.guess(clue, safe)


    def guess(self, clue, safe):
        """Try to guess a country (or teritory) from a clue
        Generally try the standard ISO 3166 parameters first,
        then try any extended parameter. """

        self.data = dict()  # Default value. If no hits are found, then no info in .data

        # Standard ISO 3166 parameter search
        if isinstance(clue, (bytes, str)):  # Clue is string type
            try:
                num_clue = int(clue)  # test if it's a number
            except ValueError:
                num_clue = None
            if num_clue:
                clue = num_clue  # if string holds a number, pass it to the number section
            elif len(clue) == 2:  # It's assumed to be an Alpha-2 code
                clue = clue.upper()  # Conveniently ignores case of uder input
                if clue in self.dic_iso3166.keys():
                    self.data = self.dic_iso3166[clue]
            elif len(clue) == 3:  # It's assumed to be an Alpha-3 code
                lst_ret = list()
                for key in self.dic_iso3166.keys():
                    if 'alpha_3' in self.dic_iso3166[key].keys() and self.dic_iso3166[key]['alpha_3'] == clue.upper():
                        lst_ret.append(self.dic_iso3166[key])
                if len(lst_ret) > 0 and (len(lst_ret) == 1 or not safe):
                    self.data = lst_ret[0]
            else:  # test for names
                lst_ret = list()
                for key in self.dic_iso3166.keys():
                    for namefield in  [tok for tok in self.dic_iso3166[key] if tok[:5].lower() == 'name_']:
                        if self.dic_iso3166[key][namefield].lower().find(clue.lower()) >= 0:
                            lst_ret.append(self.dic_iso3166[key])
                            break  # Only ad a country (teritory) once
                if len(lst_ret) > 0 and (len(lst_ret) == 1 or not safe):
                    self.data = lst_ret[0]

        if isinstance(clue, int):  # Clue is integer type
            lst_ret = list()
            for key in self.dic_iso3166.keys():
                if 'numeric_3' in self.dic_iso3166[key].keys():
                    try:
                        if int(self.dic_iso3166[key]['numeric_3']) == clue:
                            lst_ret.append(self.dic_iso3166[key])
                    except ValueError:
                        pass
            if len(lst_ret) > 0 and (len(lst_ret) == 1 or not safe):
                self.data = lst_ret[0]

    def keys(self):
        return [tok for tok in self.data.keys()]

    def get(self, key):
        if key in self.data.keys():
            return self.data[key]
        else:
            return None

    def getall(self):
        return self.data

