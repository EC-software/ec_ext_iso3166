import os

import pprint

""" EC Extendable ISO 3166 class
So far, only iso-3166-1 (country level) is implemented ...
The basic official ISO 3166-1 contains 5 fields for each country:
Numeric, Alpha_2, Alpha_3, English_name and French_name
These are all stored in the default iso3166-1.csv file.

It's easy to extend this with other fields,
e.g. the countries TLD. Se the tld.csv file for details.
This makes the TLD a fully integrated attribute on each country.

You can easily make your own extensions, by writing new .csv files,
only make sure the 1'st column is an ID that is all ready known, e.g. Alpha-2
"""

# ToDo: Clean up the many searchers, what's supposed to be the difference between guess() and find*()
#   Idea: All will: Always search ISO 3166 first, but
#   guess():
#       - Never return multiple hits (that would not be a guess)
#   locate():
#       - First and foremost, tries to be compatible with https://pypi.org/project/pycountry/
#   find():
#       - Allow for multiple returns, somehow...
#       - Allow search to target specific keys, e.g. 'capital' = 'Rome'
# ToDo: Combine find_all_by_key() and _find_all_in_any() to one function
# ToDo: Make search by number (as int) work
# ToDo: Write Test Class :-)


class Territories:

    """

    """
    def __init__(self):
        self._loaddata()

    def _add_ext_key(self, dic_in, lst_hdr, lst_new):
        """ lst_hdr are the keys, and lst_new are the values.
        In the dic_iso3166, find the entry with key_on == val_on.
        Add to this entry a new key key_new, with value val_new.
        If key_new all-ready exist, make it a list and append the new value.
        If no entry with key_on == val_on, do nothing. """
        key_on = lst_hdr[0].strip()
        val_on = lst_new[0].strip()
        key_in = lst_hdr[1].strip()
        val_in = lst_new[1].strip()
        if all([len(tok) > 0 for tok in [key_on, val_on, key_in, val_in]]):
            # print("Add_kv({}:{}) on ({}:{})".format(key_in, val_in, key_on, val_on))
            for key_te in dic_in.keys():  # Loop the Territories
                for key_old in dic_in[key_te].keys():
                    if key_old == key_on:
                        if dic_in[key_te][key_old] == val_on:  # This is the territorry to update
                            terr_upd = dic_in[key_te]
                            ##print(val_on, ">", terr_upd)
                            if key_in in terr_upd.keys():  # The 'new' key all-ready exists
                                if isinstance(terr_upd[key_in], list):  # It's all-ready a list, append.
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

    def _loaddata(self, str_data_dir='.'):
        # Read in the basic ISO 3166-1 data from the .csv file
        str_fn_iso3166 = r"iso3166-1.csv"  # file name for the basic ISO 3166 file
        sep = ','  # assumed separator in this file
        dic_iso3166 = dict()
        with open(str_fn_iso3166, 'r') as fil_iso3166:
            num_cnt = 0
            for line in fil_iso3166:
                #print(line.strip())
                line = line.split('#')[0].strip()  # Skip all comments, and spaces
                if len(line) > 0:
                    lst_in = [tok.strip() for tok in line.split(sep)]
                    if num_cnt == 0:  # Assumed to be the header
                        lst_head = lst_in
                    else:
                        str_num = lst_in[0]  # Note: We assume the first column to be the Alpha-2 id.
                        dic_iso3166[str_num] = dict()
                        for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogenious search for all parameters
                            dic_iso3166[str_num][lst_head[n]] = lst_in[n]
                    num_cnt += 1
        self._data = dic_iso3166
        print(f"Done reading base iso-3166-1 for {len(self._data)} territories")

        str_root_path = os.path.realpath(fil_iso3166.name).rsplit(os.sep, 1)[0] + os.sep  # Use this place to look for other .csv files later
        ##print(f"root_path: {str_root_path}")

        # Read the additional .csv files. NOTE: This is where the EC Extendable comes from !!!
        for root, dirs, files in os.walk(str_root_path):
            for name in files:
                if '.csv' in name and 'iso3166-1.csv' not in name:  # We all ready handled iso3166-1.csv above
                    print(f" + Extending base iso-3166-1 with: {os.path.join(root, name)}")
                    num_cnt = 0
                    with open(os.path.join(root, name), 'r') as fil_ex:
                        for line in fil_ex:
                            data = line.split('#', 1)[0]
                            if ',' in data:
                                lst_in = [tok.strip() for tok in data.split(',')]
                                if num_cnt == 0:  # Header line
                                    lst_head = lst_in
                                else:
                                    dic_iso3166 = self._add_ext_key(dic_iso3166, lst_head, lst_in)
                                num_cnt += 1

        # End of functions for reading in data...

    def get(self, id):
        """ Return a dictionary with the territory information for territory with alpha-2 = id
        if id don't exist, then return None. """
        if id in self._data.keys():
            return self._data[id]
        else:
            return None

    def categories(self):
        """ Return a list of all categories known to the class """
        set_cat = set()
        for ter in self._data.keys():
            set_cat.update(self._data[ter].keys())
        #print(f"cathegories: {set_cat}")
        return sorted(set_cat)

    def find(self, token, category=""):
        """ Allows for multiple returns, therefore always return a list.
        If no match is found for token it returns an empty list.
        Allow for
        """

    def guess(self, token):
        """ So far this is implemented as a .find()
        that returns the first element in the list, not the whole list.
        For this reason it should maintain the same parameters as find. """
        for ter in self._data:
            pass


class xTerritory(object):

    """ A Territory.
    Typically a country, but can be independent territories
    or subdivision of countries or territories. """

    # Begin Class variables and functions

    def add_ext_key(dic_in, lst_hdr, lst_new):
        """ lst_hdr are the keys, and lst_new are the values.
        In the dic_iso3166, find the entry with key_on == val_on.
        Add to this entry a new key key_new, with value val_new.
        If key_new all-ready exist, make it a list and append the new value.
        If no entry with key_on == val_on, do nothing. """
        key_on = lst_hdr[0].strip()
        val_on = lst_new[0].strip()
        key_in = lst_hdr[1].strip()
        val_in = lst_new[1].strip()
        if all([len(tok) > 0 for tok in [key_on, val_on, key_in, val_in]]):
            # print("Add_kv({}:{}) on ({}:{})".format(key_in, val_in, key_on, val_on))
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
    str_fn_iso3166 = r"iso3166-1.csv"  # file name for the basic ISO 3166 file
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
            if '.csv' in name and not 'iso3166-1.csv' in name:  # We all ready handled iso3166-1.csv above
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

    # End of functions for reading in data...


    def _compare(self, val_m, itm, safe):
        """ Compare a specific set of values.
        So far assume all in string XXX This may be a wrong assumption XXX
        Comparison is Case-Insensitive. """
        if (val_m == None or itm == None):  # Some Territories may lack a certain key
            return False
        if isinstance(val_m, (int, float)):
            print("Can't compare Numbers ...")
            return False
        if val_m.lower() == itm.lower():
            return True
        else:
            if not safe:  # Allowing partly match
                if itm.lower().find(val_m.lower()) >= 0:
                    return True
        return False

    def _kv_match_terr(self, key_f, val_m, dic_ter, safe=True):
        """ Check if a key-value pair match the territory.
        Return True on match, else False. """

        bol_match = False  # Assume no hit, until a hit is found
        if isinstance(dic_ter.get(key_f), list):
            for itm in dic_ter.get(key_f):
                if not bol_match:  # No need to go on if we all ready have a match
                    bol_match = self._compare(val_m, itm, safe)
        else:
            bol_match = self._compare(val_m, dic_ter.get(key_f), safe)
        return bol_match

    def _kv_any_match_terr(self, val_m, dic_ter, safe=True):
        """ Check if a value match any key on the territory.
        Return True on match, else False. """

        bol_match = False  # Assume no hit, until a hit is found
        for key_t in dic_ter.keys():
            if not bol_match:  # No need to go on if we all ready have a match
                if isinstance(dic_ter.get(key_t), list):
                    for itm in dic_ter.get(key_t):
                        if not bol_match:  # No need to go on if we all ready have a match
                            bol_match = self._compare(val_m, itm, safe)
                else:
                    bol_match = self._compare(val_m, dic_ter.get(key_t), safe)
        return bol_match

    # XXX ToDo: combine find_all_by_key and _find_all_in_any to one function
    def _find_all_in_any(self, val_f, safe=True):
        """ Find all territories that have val_f in any of it's keys.
        Return an (empty) list. """
        lst_ret = list()
        for key_te in self.dic_iso3166.keys():
            if self._kv_any_match_terr(val_f, self.dic_iso3166[key_te], safe):
                lst_ret.append(self.dic_iso3166[key_te])
        return lst_ret

    # XXX ToDo: combine find_all_by_key and _find_all_in_any to one function
    def _find_all_by_key(self, key_f, val_f, safe=True):
        """ Find all territories that have key_f == val_f
        Return an (empty) list. """
        lst_ret = list()
        for key_te in self.dic_iso3166.keys():
            if self._kv_match_terr(key_f, val_f, self.dic_iso3166[key_te], safe):
                lst_ret.append(self.dic_iso3166[key_te])
        return lst_ret

    # End Class variables and functions


    def __init__(self, clue="", safe=True):
        self.data = dict()
        self.guess(clue, safe)


    def guess(self, clue, safe=True):
        """ Try to guess a country (or territory) from a clue
        Generally try the standard ISO 3166 parameters first,
        then try any extended parameter.
        The found Territory will be set as self.data, and additionally returned.
        :clue: str
        :safe: bool. Only important in case of multi-hit. Safe return nothing, Un-safe returns 1'st hit.
        :rtype: dict
        :return: self.data """

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
                for key in self.dic_iso3166.keys():  # ToDo: This can be shortened...
                    if 'alpha_3' in self.dic_iso3166[key].keys() and self.dic_iso3166[key]['alpha_3'] == clue.upper():
                        lst_ret.append(self.dic_iso3166[key])
                if len(lst_ret) > 0 and (len(lst_ret) == 1 or not safe):
                    self.data = lst_ret[0]
            else:  # test for names  ToDo: Make sure we check official ISO 3166 names first!
                lst_ret = list()
                for key in self.dic_iso3166.keys():
                    for namefield in  [tok for tok in self.dic_iso3166[key] if tok[:5].lower() == 'name_']:
                        if self.dic_iso3166[key][namefield].lower().find(clue.lower()) >= 0:
                            lst_ret.append(self.dic_iso3166[key])
                            break  # Only ad a country (territory) once
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

        return self.data


    def keys(self):
        """ Return list of all keys available on this territory. """
        return [tok for tok in self.data.keys()]


    def get(self, key):
        """ Return the Value that matches the given key.
        Return None if key not found. """
        if key in self.data.keys():
            return self.data[key]
        else:
            return None


    def get_all(self):
        """ Return the entire territory dictionary structure """
        return self.data


    def find(self, clue):
        """ Maybe this should be different from lookup, e.g. more parameters like safe, multi-returns, etc."""
        return self.lookup(clue)

    def lookup(self, clue=""):
        """ You can also look up Territories case insensitively without knowing which key the value may match.
        The funcion lookup is compatible with: pycountry 18.12.8 per the description abowe. <https://pypi.org/project/pycountry/>
        ToDo: Check what pycountry do in case of multi-hits.
        :return: Territory object, or None if no hit. """
        ret = self.guess(clue, safe=False)
        if isinstance(ret, list) and len(ret) > 0:
            return ret[0]
        else:
            return None
