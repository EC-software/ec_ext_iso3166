# import shlex  # Won't work with e.g. line: "AF, AFG, 004, Afghanistan, Afghanistan (l')"
import logging
import os

logging.basicConfig(
    # format="%(asctime)s - %(levelname)s - %(message)s",  # minimum
    format="%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",  # verbose
    filename="ec_ext_iso3166.log",
    filemode="w",
    level=logging.DEBUG)
log = logging.getLogger(__name__)


""" EC Extendable ISO 3166 class
So far, only iso-3166-1 (country level) is implemented ...
The basic official ISO 3166-1 contains 5 fields for each country:
Numeric, Alpha_2, Alpha_3, English_name and French_name
These are all stored in the default iso3166-1.csv file.

It's easy to extend this with other fields,
e.g. the countries TLD. See the tld.csv file for details.
This makes the TLD a fully integrated attribute on each country.

You can easily make your own extensions, by writing new .csv files,
only make sure the 1'st column is an ID that is all ready known, e.g. Alpha-2
"""

# ToDo: Clean up the many searchers, what's supposed to be the difference between guess() and find()
#   Idea: All will: Always search ISO 3166 first, but
#   guess():
#       - Never return multiple hits (that would't be a guess, would it?)
#   locate():
#       - First and foremost, tries to be compatible with https://pypi.org/project/pycountry/
#   find():
#       - Allow for multiple returns, somehow...
#       - Allow search to target specific keys, e.g. 'capital' = 'Rome'
# ToDo: Make search by number (as int) work
# ToDo: Write Test Class :-)
# ToDo: Consider changing from .csv to .json  Pro.: A number of errors disappears, Con.: Less comments possible
# ToDo: Consider exploring one or more of the following:
#   https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
#   https://salsa.debian.org/iso-codes-team/iso-codes/-/tree/master/data
#   https://pypi.org/project/pycountry/  -- webpage of 'pycountry'
#   https://github.com/flyingcircusio/pycountry  -- repo of 'pycountry'
#   https://datahub.io/core/country-list#python

log.debug("> main()")

# CONSTANTS

# ISO_3166_1_KEYS - It is not as standard as you would think, which keys belongs to a ISO 3166-1 record :-(
# source: https://www.iso.org/glossary-for-iso-3166.html
# source: https://www.iso.org/obp/ui/#iso:code:3166:AD
# source: https://www.iso.org/obp/ui/#iso:std:iso:3166:-1:ed-3:v1:en,fr
# source: https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
# source: https://www.iso.org/obp/ui/#search
ISO_3166_1_KEYS = ["alpha_2",  # "alpha-2",  #  a two-letter code that represents a country name, recommended as the general purpose code
                   "name_short",  # name_short_en?, name_short_fr?
                   # "name_short_lower_case", -- Not in use in ec_ext_iso3166
                   # "name_short_uppercase_en", -- Not in use in ec_ext_iso3166
                   "name_full",  # name_full_en?
                   "alpha_3",  # "alpha-3",  # a three-letter code that represents a country name, which is usually more closely related to the country name
                   "alpha-4",  # a four-letter code that represents a country name that is no longer in use. The structure depends on the reason why the country name was removed from ISO 3166-1 and added to ISO 3166-3Valid for few entries, e.g. 'AN'
                   "numeric_3",  # "numeric-3",
                   "remarks",
                   "independent",
                   "territory_name",
                   "status",
                   "status_remark"]


def order_iso3166_keys(lst_keys):
    """ Order the given keys alphabetically
    If any of the ISO 3166 keys are present, they are progressed to the start, in default order. """
    lst_ref_rev = reversed([itm for itm in ISO_3166_1_KEYS])  # make a reversed copy of the constant
    if isinstance(lst_keys, list):
        lst_keys = sorted(lst_keys)
        for key_iso in lst_ref_rev:
            if key_iso in lst_keys:
                lst_keys.insert(0, lst_keys.pop(lst_keys.index(key_iso)))  # move to front of list
        return lst_keys
    else:
        return lst_keys  # if it's not a list, just return it untouched...


def _line_to_list(str_lin, sep=',', qot='"'):
    """ Split a text line in list of tokens
    Split at every occurrence of sep, but obeys qot as quotes, that wont be split.
    :param str_lin:
    :param sep:
    :param qot:
    :return: list
    """
    lst_tmp = str_lin.split(qot)
    lst_ret = list()
    for n in range(len(lst_tmp)):
        if n % 2 == 1:  # it was originally quoted
            lst_tmp[n] = f'"{lst_tmp[n]}"'  # re-insert the qot chars for later identification
            lst_tmp[n-1] = lst_tmp[n-1].strip().rstrip(',').strip()  # remove excessive sep terminating prior token
    lst_tmp = [tok for tok in lst_tmp if tok != '']  # remove the empty tokens, creates by 'sep qot' sequences
    # At this point no tokens should start or end with sep, but n=2 do if line starts with a qot, so...
    lst_tmp = [tok.strip(sep) for tok in lst_tmp]
    # Now split with sep
    for itm in lst_tmp:
        if itm[0] == qot:
            lst_ret.append(itm.strip(qot))  # add the item, but loose the quotes
        else:
            lst_ret.extend([foo.strip() for foo in itm.split(sep)])  # split and add each element
    return lst_ret


def _add_ext_key(dic_in, lst_hdr, lst_new):
    """ Adds Extended Key to the Territories
    lst_hdr are the keys, and lst_new are the values.
    In the dic_in, find the entry with key_on == val_on.
    Add to this entry a new key key_new, with value val_new.
    If key_new all-ready exist, make it a list and append the new value.
    If no entry with key_on == val_on, do nothing. """
    key_on = lst_hdr[0].strip()
    val_on = lst_new[0].strip()
    key_in = lst_hdr[1].strip()
    val_in = lst_new[1].strip()
    if any(['.nu' in slot for slot in [key_on, val_on, key_in, val_in]]):
        log.debug(f"<{lst_hdr} : {lst_new}>")
    bol_found = False
    if all([len(tok) > 0 for tok in [key_on, val_on, key_in, val_in]]):  # We have 4 valid entries
        # print("Add_kv({}:{}) on ({}:{})".format(key_in, val_in, key_on, val_on))
        for key_te in dic_in.keys():  # Loop the Territories
            if (key_on in dic_in[key_te].keys()) and (dic_in[key_te][key_on] == val_on):  # We have found the 'on'
                # print(f" on: {dic_in[key_te]}")
                terr_upd = dic_in[key_te]
                if key_in in terr_upd.keys():  # The 'new' key all-ready exists
                    if isinstance(terr_upd[key_in], list):  # It's all-ready a list, append.
                        if val_in not in terr_upd[key_in]:
                            terr_upd[key_in].append(val_in)
                    else:  # If value is new, make a list
                        if val_in != terr_upd[key_in]:
                            terr_upd[key_in] = [terr_upd[key_in], val_in]
                else:
                    terr_upd[key_in] = val_in
                dic_in[key_te] = terr_upd  # Put the updated territory back
                bol_found = True
                break  # We can't continue the loop, as we have changed dic_in
        if not bol_found:
            log.warning(f" -- Filed to find an 'ON' for {key_on}: {val_on} << {key_in} = {val_in}")
    return dic_in


class Territories:
    """ Territories are generally Countries, but also include e.g. Antarctica, Virgin Islands, Vatican state, etc. """

    def __init__(self):
        self._loaddata()

    def _loaddata(self):
        """ Read in the basic ISO 3166-1 data, and the extended data, from the .csv files """
        str_fn_iso3166 = r"ext_iso3166/data/iso3166-1.csv"  # file name for the basic ISO 3166 file
        log.info(f"loading file: {str_fn_iso3166}")
        sep = ','  # assumed separator in this file
        qot = '"'  # assumed quoting character in this file
        dic_iso3166 = dict()
        with open(str_fn_iso3166, 'r') as fil_iso3166:
            num_cnt = 0
            for line in fil_iso3166:
                line = line.split('#')[0].strip()  # Skip all comments, and spaces
                if len(line) > 0:
                    lst_in = _line_to_list(line, sep, qot)
                    if num_cnt == 0:  # Assumed to be the header
                        lst_head = lst_in
                    else:
                        str_num = lst_in[0]  # Note: We assume the first column to be the Alpha-2 id.
                        if str_num not in dic_iso3166.keys():
                            dic_iso3166[str_num] = dict()
                            for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogeneous search for all parameters
                                dic_iso3166[str_num][lst_head[n]] = lst_in[n]
                        else:
                            raise ValueError(f"key: {str_num} already exist - First column in file {str_fn_iso3166} must have unique values ...")
                    num_cnt += 1
        self._data = dic_iso3166
        log.info(f"Done reading base iso-3166-1 for {len(self._data)} territories")

        str_root_path = os.path.realpath(fil_iso3166.name).rsplit(os.sep, 1)[0] + os.sep  # Use this place to look for other .csv files later

        # Read the additional .csv files. NOTE: This is where the EC Extendable comes from !!!
        for root, dirs, files in os.walk(str_root_path):
            for name in files:
                if (name.endswith(".csv")) and ('iso3166-1.csv' not in name):  # We all ready handled iso3166-1.csv
                    log.info(f" + Extending base iso-3166-1 with: {os.path.join(root, name)}")
                    if 'capitals' in name:
                        log.debug("hit")
                    num_cnt = 0
                    with open(os.path.join(root, name), 'r') as fil_ex:
                        for line in fil_ex:
                            data = line.split('#', 1)[0]
                            if ',' in data:
                                lst_in = _line_to_list(data, sep, qot)
                                if num_cnt == 0:  # Header line
                                    lst_head = lst_in
                                else:
                                    dic_iso3166 = _add_ext_key(dic_iso3166, lst_head, lst_in)
                                num_cnt += 1
                    log.info(f"   Done reading {num_cnt} extra info lines")

        # End of functions _loaddata()

    def dump_as_text(self):
        """ Convert the entire self data structure to text format
        ToDo: Consider optional output modes, e.g. 'pretty', 'csv, 'json', other?
        :return: text string, likely with multiple lines in it...
        """
        str_ret = str()
        for key_t in sorted(self._data.keys()):
            ter = self._data[key_t]
            str_ret += f"\nTER: {ter['alpha_2']}"
            # for k in sorted(ter.keys()):
            for k in order_iso3166_keys(ter.keys()):
                str_ret += f"\n     {k}: {ter[k]}"
        return str_ret

    def get(self, str_id):
        """ Return a dictionary with the territory information for territory with alpha-2 = id
        if id don't exist, then return None. """
        if str_id in self._data.keys():
            log.warning(f"Found: {str_id} in self-data")
            return self._data[str_id]
        else:
            log.warning(f"Can't find: {str_id} in self-data")
            return None

    def categories(self):
        """ Return a list of all categories known to the class """
        set_cat = set()
        for ter in self._data.keys():
            set_cat.update(self._data[ter].keys())
        return sorted(set_cat)

    def list_missing_values(self):
        """ For each territory, list the names of the categories that are not filled, but exist for other territories.
        a categories like 'name_misc_en', that only exist for few territories, will be often mentioned here.
        ToDo: Let missing_values return list by value, in add to list by key """
        lst_cat = self.categories()
        lst_ret = list()
        for ter in sorted(self._data.keys()):
            lst_miss = [key for key in lst_cat if key not in self._data[ter].keys()]
            if len(lst_miss) > 0:
                lst_ret.append((ter, lst_miss))
        return lst_ret

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

log.debug("< main()")