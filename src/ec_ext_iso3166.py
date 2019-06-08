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


    def __init__(self, clue=""):
        self.data = dict()
        self.guess(clue)

    def guess(self, clue):
        # guess alpha code
        if len(clue) == 2:  # It's an Alpha-2 code
            if clue in self.dic_iso3166.keys():
                self.data = self.dic_iso3166[clue]
        try:
            num_clue = int(clue)
        except ValueError:
            num_clue = None
        if num_clue:
            pass

    def keys(self):
        return [tok for tok in self.data.keys()]

    def get(self, key):
        if key in self.data.keys():
            return self.data[key]
        else:
            return None

    def getall(self):
        return self.data

