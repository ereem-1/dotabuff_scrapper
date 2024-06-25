import requests
from bs4 import BeautifulSoup as Soup
from itertools import zip_longest


url = "https://www.dotabuff.com/heroes"
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)'
    'Gecko/20100101 Firefox/115.0',
           }

response2 = requests.get(url, headers=headers)
response4 = requests.get(f'{url}/lanes', headers=headers)

bs2 = Soup(response2.text, 'html.parser')
bs4 = Soup(response4.text, 'html.parser')
LIMIT = 18


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def heroes_list():
    temp = bs2.find_all('div', 'tw-flex tw-flex-col tw-gap-0')

    heroes = []
    for i in temp:
        hero = i.find_next('div').text
        heroes.append(hero)
    for i in range(len(heroes)):
        heroes[i] = heroes[i].lower().replace(' ', '-')
    return heroes


def lanes_list():
    mid_lane = bs4.find('div', class_='filter')\
                    .find('div', class_='nav').find_next('nav')\
                    .find_next('ul').find_next('li', class_='active')
    other_lanes = bs4.find('div', class_='filter').find('div', class_='nav')\
        .find_next('nav').find_next('ul')\
        .find_next('li', class_='active')\
        .find_all_next('li', class_='', limit=4)
    lanes = [mid_lane.text]
    for i in other_lanes:
        lanes.append(i.text)
    return lanes


def dotaBuffScrapping(item_id):
    response3 = requests.get(f'{url}/{item_id}', headers=headers)
    bs3 = Soup(response3.text, 'html.parser')
    temp = bs3.find('div', class_='col-8').find('section')\
        .find('tbody').find_next('tr')\
        .find_all_next('td', limit=LIMIT)
    heroes = []
    for i in temp:
        heroes.append(i.text)
    heroe_lanes = list(grouper(heroes, 6, fillvalue=None))
    heroe_lanes2 = []
    for i in range(len(heroe_lanes)):
        if heroe_lanes[i][0] in lanes_list():
            heroe_lanes2 += heroe_lanes[i]
    splitter = 6
    heroes_statistic = [heroe_lanes2[i:i + splitter]
                        for i in range(0, len(heroe_lanes2), splitter)]
    return heroes_statistic


def heroes_links():
    dictionary = {}

    for i in range(len(heroes_list())):
        dictionary[heroes_list()[i]] = f'127.0.0.1:8000/info/\
        {heroes_list()[i]}'
    return dictionary


def counterBuffScrapper(item_id):
    response5 = requests.get(f'{url}/{item_id}', headers=headers)
    bs5 = Soup(response5.text, 'html.parser')
    temp = bs5.find('div', class_='col-8').section.next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling
    heroes = []
    for i in temp.find_all('td'):
        heroes.append(i.text)

    heroe_lanes = list(grouper(heroes, 5, fillvalue=None))
    splitter = 10
    heroes_statistic = [heroe_lanes[i:i + splitter] for i in
                        range(0, len(heroe_lanes), splitter)]
    return heroes_statistic
