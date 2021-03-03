import requests
from bs4 import BeautifulSoup

import re


def get_predmet_data(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    result = {'ocjenjivanje': {}, 'komponente': []}

    divs = soup.find_all('div', attrs={'class': 'col-xs-12'})
    for div in divs:
        if "<h4>Ocjenjivanje</h4>" in str(div):

            result['ocjenjivanje']['dovoljan'] = ' '.join(
                div.find_all('strong')[3].text.split())
            result['ocjenjivanje']['dobar'] = ' '.join(
                div.find_all('strong')[2].text.split())
            result['ocjenjivanje']['vrlo_dobar'] = ' '.join(
                div.find_all('strong')[1].text.split())
            result['ocjenjivanje']['odlican'] = ' '.join(
                div.find_all('strong')[0].text.split())

    divs = soup.find_all('tbody')
    for div in divs:
        for tr in div.find_all('tr'):
            comps = []
            for td in tr.find_all('td'):
                comps.append(' '.join(td.text.split()))
            comp = [comps[x] for x in [0, 2, 3]]
            if comp[1]:
                result['komponente'].append({
                    'ime': comp[0],
                    'prag': comp[1].split(" ")[0],
                    'bodovi': comp[2].split(" ")[0],
                })

    return result
