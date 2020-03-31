
for term in [4, 26, 208]:
    if isinstance(term, int):
        term = ("000" + str(term))[-3:]
        print(term)