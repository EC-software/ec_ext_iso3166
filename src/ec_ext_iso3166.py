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

    # Read the additional .csv files. NOTE: This is where the EC Extandable comes from !!!

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
                pass


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

