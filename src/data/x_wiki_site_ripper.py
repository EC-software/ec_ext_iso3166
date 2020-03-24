
# https://gis.stackexchange.com/questions/1047/seeking-full-list-of-iso-alpha-2-and-iso-alpha-3-country-codes
# If you want to periodically update your list, you could scrape one of the sources and parse its results into a
# useful format. I've done so here for converting the Wikipedia country code list into a CSV:

import csv
import urllib3
from bs4 import BeautifulSoup

url = 'http://en.wikipedia.org/wiki/ISO_3166-1'
http = urllib3.PoolManager()
response = http.request('GET', url)
print(f"responce: {response.status}")
print(f"received: {len(response.data)} bytes")

soup = BeautifulSoup(response.data, features="html.parser")

# "Current Codes" is second table on the page
t = soup.findAll('table', {'class' : 'wikitable sortable'})[1]

# create a new CSV for the output
iso_csv = csv.writer(open('ripped_wikipedia-iso-country-codes.csv', 'w'), quoting=csv.QUOTE_MINIMAL)

# get the header rows, write to the CSV
iso_csv.writerow([th.findAll(text=True)[0].strip() for th in t.findAll('th')])

# Iterate over the table pulling out the country table results. Skip the first
# row as it contains the already-parsed header information.
for row in t.findAll("tr")[1:]:
    tds = row.findAll('td')
    raw_cols = [td.findAll(text=True) for td in tds]
    # first take the name
    cols = [raw_cols[0][1]]
    # for all other columns, use the first result text, and loose the lines shifts
    cols.extend([col[0].strip() for col in raw_cols[1:]])
    iso_csv.writerow(cols)

