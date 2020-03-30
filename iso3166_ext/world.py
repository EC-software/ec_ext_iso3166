# import shlex  # Won't work with e.g. line: "AF, AFG, 004, Afghanistan, Afghanistan (l')"
import csv
import logging
import os

logging.basicConfig(
    # format="%(asctime)s - %(levelname)s - %(message)s",  # minimum
    format="%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",  # verbose
    filename="iso3166_ext.log",
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
# ToDo: Consider:
""" EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')
    import csv
    for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
        print(emp.name, emp.title)"""
#   Idea: All will: Always search ISO 3166 first, but
#   function name x(), .returns, [] returns etc
#       - First and foremost, tries to be compatible with iso3166
#   guess():
#       - Never return multiple hits (that would't be a guess, would it?)
#   find():
#       - Allow for multiple returns, somehow... always return list, to minimise confusion.
#       - Allow search to target specific keys, e.g. 'capital' = 'Rome'
# ToDo: Make search by number (as int) work
# ToDo: Write Test Class :-)
# ToDo: Consider exploring one or more of the following:
#   https://pypi.org/project/iso3166/  <------------- Try be compatible with this !!!
#   https://en.wikipedia.org/wiki/Lists_of_country_codes
#   https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
#   https://salsa.debian.org/iso-codes-team/iso-codes/-/tree/master/data
#   https://datahub.io/core/country-list#python

log.debug("> main()")

# CONSTANTS

# The module will try to use all .tab files in the root data dictionary, and any sud-dictionary
STR_ROOT_PATH = r"iso3166_ext/data/"  # root dictionary for the data files, including the user-made files
STR_FFN_ISO3166 = STR_ROOT_PATH + "iso3166-1.tab"  # file name for the basic ISO 3166 file - leave this one as it is ...

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

IDS_REQUIRED = ['alpha_2', 'alpha_3', 'numeric_3']


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


def _add_ext_key_old(dic_in, lst_hdr, lst_new):
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


class Territory:
    """ A single territory, like Greece, Antarctica, Virgin Islands or the Vatican state. """

    def __init__(self, lst_head, lst_vals):
        """ Create a single territory from two lists. """
        self._data = dict()
        if len(lst_head) == len(set(list(lst_head))):  # Values in header must be unique
            if len(lst_head) == len(lst_vals):  # number of keys and values must match
                for n in range(len(lst_head)):
                    self._data[lst_head[n]] = lst_vals[n]
        print(f"cnf.: {self._data}")

    def add_ext_key(self, lst_head, lst_vals):
        """ Add one or more key-val sets to the Territory, based on an existing primary key.
        First key in lst_head must be a valid Prim. key. """
        pass

    def keys(self):
        """ Return a list of all keys known to the class """
        return self._data.keys()

    def as_text(self):
        str_ret = str()  # Initialising the return object
        ter = self._data
        str_ret += f"\tTER: {ter['alpha_2']}\n"
        for k in sorted(ter.keys()):
            str_ret += f"\t\t{k}: {ter[k]}\n"
        return str_ret.strip()

class Territories:
    """ Territories are generally Countries, but also include e.g. Antarctica, Virgin Islands, Vatican state, etc. """

    def __init__(self):
        self._lst_pk = list()  # List of validated primary keys
        self._data = dict()  # We use a dict(), not a tuple, as we need to modify it
        self._load_data()  # Load data from the .tab files

    def _load_data(self):
        """ Read in the basic ISO 3166-1 data, and the extended data, from the .tab files """

        def _decomment(csvfile):
            for row in csvfile:
                raw = row.split('#')[0].strip()
                if raw:
                    yield raw

        def _read_base_file():
            num_row = 0  # Number of records, assume to grow to ca. 249 (number of iso 3166-1 codes on the planet)
            num_col = 0  # Number of fields, assumed 0 until we see the header. Will likely grow to around 5
            with open(STR_FFN_ISO3166) as fil_iso3166:
                for lst_lin in csv.reader(_decomment(fil_iso3166), delimiter="\t"):
                    # log.debug(lst_lin)
                    if num_row == 0:  # assume this to be the header
                        lst_head = lst_lin
                        num_col = len(lst_head)
                        if all([tok in lst_head for tok in IDS_REQUIRED]):  # Header is ID-complete
                            log.info(f"Header is: {lst_head}")
                        else:
                            str_msg = f"ERR: Header in file: {STR_FFN_ISO3166} do not contain all items in {IDS_REQUIRED}"
                            log.error(str_msg)
                            raise Exception(str_msg)
                    else:
                        str_first_key = lst_lin[0]  # assume the first column to be the Alpha-2 id.
                        if str_first_key not in self._data.keys():
                            self._data[str_first_key] = Territory(lst_head, lst_lin)
                            # for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogeneous search for all parameters
                            #     self._data[str_first_key][lst_head[n]] = lst_lin[n]
                        else:
                            str_msg = f"key: {str_first_key} already exist - First column in file {STR_FFN_ISO3166} must have unique values ..."
                            log.error(str_msg)
                            raise ValueError(str_msg)
                    num_row += 1
            # Establish and confirm primary keys by looking at all 'prime key candidates'
            for str_pkc in lst_head:
                pass

        def _read_xtnd_file(str_fn):
            num_row = 0  # Number of records, assume to grow to ca. 249 (number of iso 3166-1 codes on the planet)
            num_col = 0  # Number of fields, assumed 0 until we see the header. Will likely grow to around 5
            with open(str_fn) as fil_xtnd:
                for lst_lin in csv.reader(_decomment(fil_xtnd), delimiter="\t"):
                    log.debug(lst_lin)
                    if num_row == 0:  # assume this to be the header
                        lst_head = lst_lin
                        if lst_head[0] not in self.prim_keys():  # First column must be existing, valid prim. key.
                            log.warning(f"Warning: First key (column): {lst_head[0]} "
                                        f"in file: {str_fn} is not a valid prim. key, at this time ...")
                            return str_fn
                    else:
                        self._add_ext_key(lst_head, lst_lin)
                        # str_first_key = lst_lin[0]  # assume the first column to be the Alpha-2 id.
                        # if str_first_key not in self._data.keys():
                        #     self._data[str_first_key] = dict()
                        #     for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogeneous search for all parameters
                        #         self._data[str_first_key][lst_head[n]] = lst_lin[n]
                        # else:
                        #     str_msg = f"key: {str_first_key} already exist - First column in file {STR_FFN_ISO3166} must have unique values ..."
                        #     log.error(str_msg)
                        #     raise ValueError(str_msg)
                    num_row += 1
            return None  # Indicating that all went Okay

        log.info(f"Start Loading base iso-3166-1")
        log.info(f"Start reading file: {STR_FFN_ISO3166}")
        _read_base_file()  # Will load the base file into self._data
        log.info(f"Done: reading file: {STR_FFN_ISO3166}")

        print(f"debug: post iso3166-1.tab\t> {self._data['GB']}")

        # Read the additional .tab files. NOTE: This is where the Extendable comes from !!!
        log.info(f"Start Loading Extended iso-3166-1 info ...")
        for root, dirs, files in os.walk(STR_ROOT_PATH):
            for str_fn in files:
                if (str_fn.endswith(".tab")) and ('iso3166-1.tab' not in str_fn):  # We all ready handled iso3166-1.csv
                    str_ffn = os.path.join(root, str_fn)
                    log.info(f"Start reading file: {str_fn}")
                    print(f"EXT file: {str_ffn}")
                    _read_xtnd_file(str_ffn)
                    # num_cnt = 0
                    # with open(os.path.join(root, str_fn), 'r') as fil_ex:
                    #     for line in fil_ex:
                    #         # print(line.strip())
                    #         data = line.split('#', 1)[0]
                    #         if ',' in data:
                    #             lst_in = _line_to_list(data, sep, qot)
                    #             if num_cnt == 0:  # Header line
                    #                 lst_head = lst_in
                    #             else:
                    #                 dic_iso3166 = _add_ext_key(dic_iso3166, lst_head, lst_in)
                    #             num_cnt += 1
                    log.info(f"Done: reading file: {os.path.join(root, str_fn)}")
                    print(f"debug: post {str_fn}\t> {self._data['GB']}")

        log.info(f"Done: Loading base iso-3166-1 for {len(self._data)} territories")

    def _add_ext_key(self, lst_head, lst_keva):
        """ Add new key(s) to a territory.
        Do the hard work by calling the territory's own add function. """
        ter = self._data[lst_head[0]]
        ter = ter.add_ect_key(lst_head, lst_keva)
        self._data[lst_head[0]] = ter

    def prim_keys(self):
        return self._lst_pk

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
