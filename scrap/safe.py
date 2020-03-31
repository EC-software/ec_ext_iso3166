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
    if all([len(tok) > 0 for tok in [key_on, val_on, key_in, val_in]]):  # We have 4 valid entries
        print("Add_kv({}:{}) on ({}:{})".format(key_in, val_in, key_on, val_on))
        for key_te in dic_in.keys():  # Loop the Territories
            print(f" X: {dic_in[key_te]}")
            for key_old in dic_in[key_te].keys():
                if key_old == key_on:
                    if dic_in[key_te][key_old] == val_on:  # This is the territorry to update
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
                        break  # We can't continue the loop, as we have changed dic_in
    return dic_in