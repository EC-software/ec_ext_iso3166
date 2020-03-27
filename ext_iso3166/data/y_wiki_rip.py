import json

import bs4
import requests

print(json.dumps(
    [
        {
            ['name', 'alpha_2', 'alpha_3', 'numeric'][no]:
            td.find_all()[-1].text
            for no, td in enumerate(row.find_all('td')[:-1])
        }
        for row in bs4.BeautifulSoup(
            requests.get('http://en.wikipedia.org/wiki/ISO_3166-1').text
        ).find('table', {'class': 'wikitable sortable'}).find_all('tr')[1:]
    ],
    indent=4,
    ensure_ascii=False
))