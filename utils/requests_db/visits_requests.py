import requests_cache
from bs4 import BeautifulSoup
from love_bot.database.requests.visit import set_visit


def req_visit(url):
    session = requests_cache.CachedSession()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'lxml')
    main_div = soup.find('div', class_='content-inner')
    arr = main_div.find_all('p')[9:]
    return arr


async def add_visits():
    arr = req_visit('https://mensby.com/women/relations/romanticheskoe-svidanie-dlja-dvoih-list-romanticheskij-idej-dlja-vechera-c-devushkoj')
    for visit in arr:
        await set_visit(visit.text)
