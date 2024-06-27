import requests
from bs4 import BeautifulSoup as Soup
from itertools import zip_longest


url = "https://www.dotabuff.com/heroes"
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)'
    'Gecko/20100101 Firefox/115.0',
           }

response_site = requests.get(url, headers=headers)
response_lanes = requests.get(f'{url}/lanes', headers=headers)

bs_site = Soup(response_site.text, 'html.parser')
bs_lanes = Soup(response_lanes.text, 'html.parser')
LIMIT = 18


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def heroes_list():
    temp = bs_site.find_all('div', 'tw-flex tw-flex-col tw-gap-0')

    heroes = []
    for i in temp:
        hero = i.find_next('div').text
        heroes.append(hero)
    for i in range(len(heroes)):
        heroes[i] = heroes[i].lower().replace(' ', '-')
    return heroes


def lanes_list():
    mid_lane = bs_lanes.find('div', class_='filter')\
                    .find('div', class_='nav').find_next('nav')\
                    .find_next('ul').find_next('li', class_='active')
    other_lanes = bs_lanes.find('div', class_='filter')\
        .find('div', class_='nav')\
        .find_next('nav').find_next('ul')\
        .find_next('li', class_='active')\
        .find_all_next('li', class_='', limit=4)
    lanes = [mid_lane.text]
    for i in other_lanes:
        lanes.append(i.text)
    return lanes


def dotaBuffScrapping(item_id):
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
    splitter = 6
    heroes_statistic = [heroe_lane2[i:i + splitter]
                        for i in range(0, len(heroe_lane2), splitter)]
    return heroes_statistic


def heroes_links():
    dictionary = {}

    for i in range(len(heroes_list())):
        dictionary[heroes_list()[i]] = f'127.0.0.1:8000/info/\
        {heroes_list()[i]}'
    return dictionary


def counterBuffScrapper(item_id):
    c =[]
    response_counter = requests.get(f'{url}/{item_id}', headers=headers)
    bs_counter = Soup(response_counter.text, 'html.parser')
    temp = bs_counter.find('div', class_='col-8').section.next_sibling\
        .next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.next_sibling\
        .next_sibling.tbody.tr
    # temp = bs_counter.find_next_sibling("tr")
    nextSiblings = temp.next_siblings
    for nextSibling in nextSiblings:
        # temp.next_sibling.next_sibling
        for next in nextSibling:
            c.append(next.text)
    for i in c:
        if i == '':
            c.remove(i)
    counter_statistic = list(grouper(c, 4, fillvalue=None))
    return counter_statistic

            # print(next.text)
    # return temp.text
    # heroes = []
    # for i in temp.find_all('td'):
    #     heroes.append(i.text)

    # heroe_lanes = list(grouper(heroes, 5, fillvalue=None))
    # splitter = 10
    # heroes_statistic = [heroe_lanes[i:i + splitter] for i in
    #                     range(0, len(heroe_lanes), splitter)]
    # return heroes_statistic

print(counterBuffScrapper('io'))
# counterBuffScrapper('io')
# uniq = [1,2,3,4,5]
# fifa = ['a','b','c','d','e']
# uniq_and_fifa = dict(zip(uniq, fifa))
# print(uniq_and_fifa)
titles = ['Lane', 'Presence', 'Win Rate', 'KDA', 'GPM', 'XPM']
# titles_and_statistics = dict(zip(titles, dotaBuffScrapping('lifestealer')))
# print(titles_and_statistics)
# print(dotaBuffScrapping('io'))
# print(len(dotaBuffScrapping('io')[0]))


def statistics_dict(item_id):
    for a in range(len(dotaBuffScrapping(item_id))):
            b = dict(zip(titles, dotaBuffScrapping(item_id)[a]))
            c = dict(zip(titles, dotaBuffScrapping(item_id)[a+1]))
            d = dict(zip(titles, dotaBuffScrapping(item_id)[a+2]))
        # dotaBuffScrapping(item_id)
        # break
    return b, c, d
# for i in dotaBuffScrapping('io')[0]:
#     print(i)
# print(dotaBuffScrapping('io'))
# print(statistics_dict('abaddon'))
# statistics_dict('io')
# print(b)
# def counterBuffScrapper(item_id):
#     response_counter = requests.get(f'{url}/{item_id}', headers=headers)
#     bs_counter = Soup(response_counter.text, 'html.parser')
#     temp = bs_counter.find('div', class_='col-8').section.next_sibling\
#         .next_sibling\
#         .next_sibling.next_sibling\
#         .next_sibling.next_sibling\
#         .next_sibling.next_sibling\
#         .next_sibling
#     heroes = []
#     for i in temp.find_all('td'):
#         heroes.append(i.text)

#     heroe_lanes = list(grouper(heroes, 5, fillvalue=None))
#     splitter = 10
#     heroes_statistic = [heroe_lanes[i:i + splitter] for i in
#                         range(0, len(heroe_lanes), splitter)]
#     return heroes_statistic