import requests
from bs4 import BeautifulSoup as Soup
from itertools import zip_longest


url = "https://www.dotabuff.com/heroes"
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)'
    'Gecko/20100101 Firefox/115.0',
           }

LIMIT = 18
LIMIT_LANES = 4
SPLITTER_HERO = 6
SPLITTER_COUNTER = 4
titles = ['Lane', 'Presence', 'Win Rate', 'KDA', 'GPM', 'XPM']
counterpicks = ['Hero', 'Disadvantage', 'Win Rate', 'Matches']
response_site = requests.get(url, headers=headers)
response_lanes = requests.get(f'{url}/lanes', headers=headers)
bs_site = Soup(response_site.text, 'html.parser')
bs_lanes = Soup(response_lanes.text, 'html.parser')

'''Функция групировки/разбиения списка на одинаковое количество списков'''


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


'''Функция, которая при выполнении получает список героев'''


def heroes_list() -> list:
    temp = bs_site.find_all('div', 'tw-flex tw-flex-col tw-gap-0')
    heroes = []
    for i in temp:
        hero = i.find_next('div').text
        heroes.append(hero)
    for i in range(len(heroes)):
        heroes[i] = heroes[i].lower().replace(' ', '-')
    return heroes


'''Функция, которая получает список линий'''


def lanes_list() -> list:
    mid_lane = bs_lanes.find('div', class_='filter')\
                    .find('div', class_='nav').find_next('nav')\
                    .find_next('ul').find_next('li', class_='active')
    other_lanes = bs_lanes.find('div', class_='filter')\
        .find('div', class_='nav')\
        .find_next('nav').find_next('ul')\
        .find_next('li', class_='active')\
        .find_all_next('li', class_='', limit=LIMIT_LANES)
    lanes = [mid_lane.text]
    for i in other_lanes:
        lanes.append(i.text)
    return lanes


'''Функция, которая на выходе возвращает статистику героя на линиях'''


def dotaBuffScrapping(item_id: str) -> list:
    response_hero = requests.get(f'{url}/{item_id}', headers=headers)
    bs_hero = Soup(response_hero.text, 'html.parser')
    temp = bs_hero.find('div', class_='col-8').find('section')\
        .find('tbody').find_next('tr')\
        .find_all_next('td', limit=LIMIT)
    heroes = []
    for i in temp:
        heroes.append(i.text)
    heroe_lane = list(grouper(heroes, 6, fillvalue=None))
    heroe_lane2 = []
    for i in range(len(heroe_lane)):
        if heroe_lane[i][0] in lanes_list():
            heroe_lane2 += heroe_lane[i]
    heroes_statistic = [heroe_lane2[i:i + SPLITTER_HERO]
                        for i in range(0, len(heroe_lane2), SPLITTER_HERO)]
    return heroes_statistic


''''Функция, котоорая создает словарь,
где ключ это герой, а значение - ссылка на него'''


# def heroes_links() -> dict:
#     dictionary = {}
#     for i in range(len(heroes_list())):
#         dictionary[heroes_list()[i]] = f'127.0.0.1:8000/info/\
#         {heroes_list()[i]}'
#     return dictionary


'''Функция, которая возвращает статистику контрпиков героя'''


def counterBuffScrapper(item_id: str) -> list:
    c = []
    response_counter = requests.get(f'{url}/{item_id}', headers=headers)
    bs_counter = Soup(response_counter.text, 'html.parser')
    temp = bs_counter.find('div', class_='col-8').section.next_sibling\
        .next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.tbody.tr
    nextSiblings = temp.next_siblings
    for nextSibling in nextSiblings:
        for next in nextSibling:
            c.append(next.text)
    for i in c:  # Удаление пробелов из списка контрпиков
        if i == '':
            c.remove(i)
    counter_statistic = list(grouper(c, SPLITTER_COUNTER, fillvalue=None))
    return counter_statistic
