# with open('name_short_en__wiki.csv', 'r') as log_file_fh:
#     for line in log_file_fh:
#         print(line)

lin = 0
pos = 0
with open('Spanish.csv_later', 'r', encoding='cp850') as log_file_fh:
    for line in log_file_fh:
        print(f"lp:{lin}:{pos}| {line.strip()}")
        lin += 1
        pos += len(line)+1