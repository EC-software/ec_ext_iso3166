

# def _line_to_list(str_lin, sep=',', qot='"'):
#     """ Split a text line in list of tokens
#     Split at every occurrence of sep, but obeys qot as quotes, that wont be split.
#     :param str_lin:
#     :param sep:
#     :param qot:
#     :return: list
#     """
#     lst_tmp = str_lin.split(qot)
#     lst_ret = list()
#     for n in range(len(lst_tmp)):
#         if n % 2 == 1:  # it was originally quoted
#             lst_tmp[n] = f'"{lst_tmp[n]}"'  # re-insert the qot chars for later identification
#             lst_tmp[n-1] = lst_tmp[n-1].strip().rstrip(',').strip()  # remove excessive sep terminating prior token
#     lst_tmp = [tok for tok in lst_tmp if tok != '']  # remove the empty tokens, creates by 'sep qot' sequences
#     # At this point no tokens should start or end with sep, but n=2 do if line starts with a qot, so...
#     lst_tmp = [tok.strip(sep) for tok in lst_tmp]
#     # Now split with sep
#     for itm in lst_tmp:
#         if itm[0] == qot:
#             lst_ret.append(itm.strip(qot))  # add the item, but loose the quotes
#         else:
#             lst_ret.extend([foo.strip() for foo in itm.split(sep)])  # split and add each element
#     return lst_ret

