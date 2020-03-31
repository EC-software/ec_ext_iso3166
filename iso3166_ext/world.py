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
ISO_3166_1_KEYS = ['alpha_2',  # 'alpha-2',  #  a two-letter code that represents a country name, recommended as the general purpose code
                   'name_short',  # name_short_en?, name_short_fr?
                   # 'name_short_lower_case', -- Not in use in ec_ext_iso3166
                   # 'name_short_uppercase_en', -- Not in use in ec_ext_iso3166
                   'name_full',  # name_full_en?
                   'alpha_3',  # 'alpha-3',  # a three-letter code that represents a country name, which is usually more closely related to the country name
                   'alpha-4',  # a four-letter code that represents a country name that is no longer in use. The structure depends on the reason why the country name was removed from ISO 3166-1 and added to ISO 3166-3Valid for few entries, e.g. 'AN'
                   'numeric_3',  # 'numeric-3',
                   'remarks',
                   'independent',
                   'territory_name',
                   'status',
                   'status_remark']

IDS_REQUIRED = ['alpha_2', 'alpha_3', 'numeric_3']  # All Territory should have valid values for these key ID fields.
ID_PREFERRED = 'alpha_2'  # Any required ID could potentially take this place, but this one have been selected!


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


class Territory:
    """ A single territory, like Greece, Antarctica, Virgin Islands or the Vatican state. """

    # ToDo: Consider functions to Update and/or Delete values of a Territory

    def __init__(self, lst_head, lst_vals):
        """ Create a single territory from two lists. """
        ##print(lst_head, lst_vals)
        self._data_teri = dict()
        if len(lst_head) == len(set(list(lst_head))):  # Values in header must be unique
            if len(lst_head) == len(lst_vals):  # number of keys and values must match
                for n in range(len(lst_head)):
                    self._data_teri[lst_head[n]] = lst_vals[n]
        ##print(f"cnf.: {self._data_teri}")

    def add_ext_key(self, lst_head, lst_vals):
        """ Add one or more key-val sets to the Territory, based on an existing primary key.
        First key in lst_head must be a valid Prim. key. - but that is a property of the entire Territories instance.
        First key also have to be amongst the existing keys, and we can check that.
        The two lists need to have same length. """
        if len(lst_head) == len(lst_vals):
            if lst_head[0] in self.keys():
                for n in range(len(lst_head)):
                    if n > 0:  # don't update the prim. key
                        if lst_head[n] not in self.keys():  # it's a brand new key, just put it in
                            self._data_teri[lst_head[n]] = lst_vals[n]
                        else:  # key already exists, we need a list
                            if isinstance(self._data_teri[lst_head[n]], list):  # it's already a list
                                ret_val = self._data_teri[lst_head[n]]
                            else:  # we put existing value in a list
                                ret_val = [self._data_teri[lst_head[n]]]
                            ret_val.append(lst_vals[n])  # we add the new value to the list
                            ret_val = list(set(ret_val))  # eliminate duplicate values
                            if len(ret_val) == 1:
                                ret_val = ret_val[0]  # if list of one value, take it out of the list
                            self._data_teri[lst_head[n]] = ret_val  # return the updated list to data collection, while removing duplicates
            else:
                log.warning(f"add_ext_key() can't add, if first key: {lst_head[0]} "
                            f"is not an primary key for the Territory: {self.keys()}")
        else:
            log.warning(f"add_ext_key() can't add, if not same number of keys and vals {lst_head} <> {lst_vals}")

    def keys(self):
        """ Return a list of all keys known to the class """
        return self._data_teri.keys()

    def values(self):
        """ Return a list of all values from the class """
        return self._data_teri.values()

    def get(self, str_key):
        if str_key in self.keys():
            return self._data_teri[str_key]
        else:
            log.warning(f"get() can't deliver, because key: {str_key} is not in keys(): {self.keys()}")

    def as_text(self):
        str_ret = str()  # Initialising the return object
        ter = self._data_teri
        str_ret += f"\tTER: {ter[ID_PREFERRED]}\n"
        for k in sorted(ter.keys()):
            str_ret += f"\t\t{k}: {ter[k]}\n"
        return str_ret.strip()

class Territories:
    """ Territories (plural) is a collection of Territory-objects.
    Territory-objects are generally Countries, but also include e.g. Antarctica, Virgin Islands, Vatican state, etc. """

    def __init__(self):
        self._data_ters = dict()  # We use a dict(), not a tuple, as we need to modify it
        self._lst_k = list()  # Initialise list of keys present in any Territory object
        self._lst_pk = list()  # Initialise list of validated primary keys
        self._load_data()  # Load the data files
        self._update_inner_k()
        self._update_inner_pk()

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
                for lst_lin in csv.reader(_decomment(fil_iso3166), delimiter='\t'):
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
                        if str_first_key not in self._data_ters.keys():
                            self._data_ters[str_first_key] = Territory(lst_head, lst_lin)
                            # for n in range(len(lst_head)):  # Note that Alpha-2 is loaded again, to allow homogeneous search for all parameters
                            #     self._data_ters[str_first_key][lst_head[n]] = lst_lin[n]
                        else:
                            str_msg = f"key: {str_first_key} already exist - First column in file {STR_FFN_ISO3166} must have unique values ..."
                            log.error(str_msg)
                            raise ValueError(str_msg)
                    num_row += 1
            # Establish and confirm inner primary keys by looking at all 'inner prime key candidates'
            self._update_inner_pk()
            ##log.debug(f"x1 inner_k  {self.inner_keys()}")
            ##log.debug(f"x1 inner_pk {self.inner_prim_keys()}")
            ##log.debug(f"x1 self.keys(): {len(self.keys())}:{sorted(self.keys())}")

        def _read_xtnd_file(str_fn):
            num_row = 0  # Number of records, assume to grow to ca. 249 (number of iso 3166-1 codes on the planet)
            num_col = 0  # Number of fields, assumed 0 until we see the header. Will likely grow to around 5
            with open(str_fn) as fil_xtnd:
                for lst_lin in csv.reader(_decomment(fil_xtnd), delimiter='\t'):
                    ##log.debug(f"xtnd_line: {lst_lin}")
                    if num_row == 0:  # assume this to be the header
                        lst_head = [tok.strip() for tok in lst_lin]  # trip whitespaces
                        tmp_val_prim = self.inner_prim_keys()
                        if lst_head[0] not in tmp_val_prim:  # First column must be existing, valid prim. key.
                            log.warning(f"Warning: First key (column): {lst_head[0]} "
                                        f"in file: {str_fn} is not a valid prim. key, at this time ...")
                            return str_fn
                        str_msg = f"accepted header: {lst_head}"
                        log.info(str_msg)
                        ##print(str_msg)
                    else:
                        self._add_ext_key(lst_head, [tok.strip() for tok in lst_lin])  # add while trimming whitespaces
                    num_row += 1
            self._update_inner_pk()
            ##log.debug(f"x2 inner_k  {self.inner_keys()}")
            ##log.debug(f"x2 inner_pk {self.inner_prim_keys()}")
            ##log.debug(f"x2 self.keys(): {len(self.keys())}:{sorted(self.keys())}")
            return None  # Indicating that all went Okay

        log.info(f"Start Loading base iso-3166-1")
        log.info(f"Start reading file: {STR_FFN_ISO3166}")
        _read_base_file()  # Will load the base file into self._data_ters
        log.info(f"Done: reading file: {STR_FFN_ISO3166}\n")

        print(f"debug: post iso3166-1.tab\t-> {self._data_ters['GB'].as_text()}")

        # Read the additional .tab files. NOTE: This is where the Extendable comes from !!!
        log.info(f"Start Loading Extended iso-3166-1 info ...")
        for root, dirs, files in os.walk(STR_ROOT_PATH):
            for str_fn in files:
                if (str_fn.endswith(".tab")) and ('iso3166-1.tab' not in str_fn):  # We all ready handled iso3166-1.csv
                    str_ffn = os.path.join(root, str_fn)
                    log.info(f"Start reading file: {str_fn}")
                    _read_xtnd_file(str_ffn)
                    log.info(f"Done: reading file: {os.path.join(root, str_fn)}\n")

                    print(f"debug: post {str_fn}\t-> {self._data_ters['GB'].as_text()}")

        log.info(f"Done: Loading base iso-3166-1 for {len(self._data_ters)} territories")

    def keys(self):
        """ Return list of all keys, i.e. list of the ID_PREFERRED for each Territory-obj. in Territories """
        return self._data_ters.keys()

    def _update_inner_k(self):
        """ Update inner keys
         Inner keys are the keys of each Territory object's ._data_teri dictionary """
        set_ik = set()  # Initialise set of all inner keys
        for key_ter in self.keys():  # Note: key_ter is an outer key
            ter = self._data_ters[key_ter]
            for key_t in ter.keys():  # Note: key_t is an inner key
                set_ik.add(key_t)
        self._lst_k = list(set_ik)

    def _update_inner_pk(self):
        """ Update list of Validated Primary keys, from list of inner keys
        For a key to qualify, it must:
        1) be represented, with a single, non-empty value, in all member Territory objects
        2) hold a unique value for every Territory objects, i.e. no two Territory objects can have the same value. """
        
        def empty(itm):
            if not itm or itm == '' or itm == 0 or itm == []:
                return True
            else:
                return False

        self._update_inner_k()  # Always make sure self._lst_k is up-to-date
        set_ppk = set(self._lst_k)  # Any candidate key is a ppk (potential primary key), until proven otherwise
        ##log.debug(f"_update_inner_pk(): initial set: {set_ppk}")
        for ppk in list(set_ppk):  # make a list from the set, to avoid editing the set while loping it
            lst_all = list()  # list for uniqueness check
            for key_ter in self.keys():  # test that all Territory objects have the key
                ter = self._data_ters[key_ter]
                if ppk not in ter.keys():
                    set_ppk.discard(ppk)
                    log.info(f"update_inner_k(): {ppk} is not prim. key, because it's not represented in {key_ter}")
                    break  # No need to look further, ppk is dis-qualified
                if isinstance(ter.get(ppk), list):
                    set_ppk.discard(ppk)
                    log.info(f"update_inner_k(): {ppk} is not prim. key, because the value is a list in {key_ter}")
                    break  # No need to look further, ppk is dis-qualified
                if empty(ter.get(ppk)):
                    set_ppk.discard(ppk)
                    log.info(f"update_inner_k(): {ppk} is not prim. key, because the value is empty in {key_ter}")
                    break  # No need to look further, ppk is dis-qualified
                # remember this value for later uniqueness check
                lst_all.append(ter.get(ppk))
            # Uniqueness check
            num_cnt_ter = len(self.keys())  # total number of keys in Territories
            num_cnt_unq = len(set([str(itm) for itm in lst_all]))  # make string while counting, as list-of-list is not hashable
            if num_cnt_unq != num_cnt_ter:  # test for uniqueness
                set_ppk.discard(ppk)
        self._lst_pk = list(set_ppk)  # update the _lst_pk value on self.
        log.info(f"update_inner_k(): Valid inner keys, i.e. Primary keys for attaching new data, are: {set_ppk}")

    def _add_ext_key(self, lst_keys, lst_vals):
        """ Add new key(s) to a territory.
        Do the hard work by calling the territory's own add function.
        It should have been checked beforehand that lst_keys[0] is a valid prim. key, not here, since this will run for each line.
        """
        ##log.debug(f"_add_ext_key({lst_keys}, {lst_vals}")
        ter = self.guess(lst_vals[0], categories=[lst_keys[0]])  # Guess will be unique, because lst_keys[0] is a valid prim. key!
        if ter:
            ter.add_ext_key(lst_keys, lst_vals)  # update the Territory
            self._data_ters[ter.get(ID_PREFERRED)] = ter  # return the Territory to Territories

    def inner_keys(self):
        return self._lst_k

    def inner_prim_keys(self):
        return self._lst_pk

    def dump_as_text(self):
        """ Convert the entire self data structure to text format
        ToDo: Consider optional output modes, e.g. 'pretty', 'csv, 'json', other?
        :return: text string, likely with multiple lines in it...
        """
        str_ret = str()
        for key_t in sorted(self._data_ters.keys()):
            ter = self._data_ters[key_t]
            str_ret += f"\nTER: {ter[ID_PREFERRED]}"
            # for k in sorted(ter.keys()):
            for k in order_iso3166_keys(ter.keys()):
                str_ret += f"\n     {k}: {ter[k]}"
        return str_ret

    def get(self, str_id):
        """ Return a dictionary with the territory information for territory with alpha-2 = id
        if id don't exist, then return None. """
        if str_id in self._data_ters.keys():
            return self._data_ters[str_id]
        else:
            log.warning(f"Can't find: {str_id} in self-data")
            return None

    def categories(self):
        """ Return a list of all categories known to the class """
        set_cat = set()
        for ter in self._data_ters.keys():
            set_cat.update(self._data_ters[ter].keys())
        return sorted(set_cat)

    def list_missing_values(self):
        """ For each territory, list the names of the categories that are not filled, but exist for other territories.
        a categories like 'name_misc_en', that only exist for few territories, will be often mentioned here.
        ToDo: Let missing_values return list by value, in add to list by key """
        lst_cat = self.categories()
        lst_ret = list()
        for ter in sorted(self._data_ters.keys()):
            lst_miss = [key for key in lst_cat if key not in self._data_ters[ter].keys()]
            if len(lst_miss) > 0:
                lst_ret.append((ter, lst_miss))
        return lst_ret

    def find(self, token, categories=[]):
        """ Allows for multiple returns, therefore always return a list.
        If no match is found for token it returns an empty list.
        Allow for categories ...
        ToDo: Find a better word for categories
        :param token: str: The phrase to look for
        :param categories: list: If non-empty, limit the search to these fields
        :return: a list of Territory object, that meet the criteria. The list can be empty
        """
        ##log.debug(f"find({token}, {categories})")
        lst_ret = list()  # Initialise the return object
        if len(categories) == 0:
            cats = set(self.inner_keys())
        else:
            cats = set(categories)
        ##log.debug(f"find()   cats: {cats}")
        for key_ter in self.keys():  # for each Territory key in Territories
            ##log.debug(f"find()   keyt: {key_ter}")
            ter = self.get(key_ter)
            for cat in (cats & set(ter.keys())):  # the intersection of the two sets
                if ter.get(cat) == token:
                    lst_ret.append(self.get(key_ter))
                    ##log.debug(f"find()   HIT: {key_ter} <------------- HIT")
                    break  # No reason to test more categories
        ##log.debug(f"find()   ret: {lst_ret}")
        return lst_ret

    def guess(self, token, categories):
        """ So far this is implemented as a .find()
        that returns the first element in the list, not the whole list.
        For this reason it should maintain the same parameters as find. """
        # ToDo: Consider return self.find(token, category)[:0] or something, to make it all a one-liner
        ##log.debug(f"guess({token}, {categories})")
        lst_suggestion = self.find(token, categories)
        if len(lst_suggestion) > 0:
            ##log.debug(f"guess() ret: {lst_suggestion[0]}")
            return lst_suggestion[0]
        else:
            ##log.debug(f"guess() ret: []")
            return None


log.debug("< main()")
