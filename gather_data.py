from selenium import webdriver
import datetime
import requests
from bs4 import BeautifulSoup


def get_obj_id(text: str):
    word_list = text.split("/")
    for _ in word_list:
        if _.isdigit():
            return _
    return None


def get_soup_lxml(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, features='lxml')


# обновление списков названий игр - основного и альтернативных
def update_boardgame_titles(game, info_dict):
    primary_name, other_names = [], []
    request = game.find_all('name')
    for item in request:
        try:
            if item['primary'] == "true":
                primary_name.append(item.text)
                continue
        except KeyError:
            pass
        other_names.append(item.text)
    info_dict['title'] = primary_name
    info_dict['other_titles'] = other_names


# обновление списков ключей без objectid
def update_boardgame_ess_wo_ids(game, info_dict):
    ess_keys_wo_oid = ['yearpublished',
                       'minplayers',
                       'maxplayers',
                       'minplaytime',
                       'maxplaytime',
                       'age',
                       'thumbnail',
                       'image',
                       'description',
                       ]
    for key in ess_keys_wo_oid:
        request = game.find_all(key)
        if request:
            for item in request:
                info_dict[key].append(item.text)


# обновление важных списков ключей с objectid
def update_boardgame_ess_with_ids(game, info_dict):
    ess_keys_with_oid = ['boardgamepublisher',
                         'boardgamedesigner',
                         'boardgameartist',
                         'boardgamemechanic',
                         'boardgamefamily',
                         'boardgamecategory',
                         'boardgamesubdomain',
                         'boardgameintegration',
                         'boardgameexpansion',
                         ]
    for key in ess_keys_with_oid:
        request = game.find_all(key)
        if request:
            for item in request:
                try:
                    if item['inbound']:
                        continue
                except KeyError:
                    tmp_dict = {'id': item['objectid'],
                                'name': item.text,
                                }
                    info_dict[key].append(tmp_dict)
        info_dict[key] = sorted(info_dict[key], key=lambda category: category['name'])
    info_dict['boardgame'] = info_dict['boardgameintegration']
    del info_dict['boardgameintegration']


# обновление неважных списков ключей с objectid
def update_boardgame_not_ess_with_ids(game, info_dict):
    not_ess_keys_with_oid = ['boardgamehonor',
                             'boardgamepodcastepisode',
                             'boardgameversion',
                             'boardgameaccessory',
                             ]
    for key in not_ess_keys_with_oid:
        request = game.find_all(key)
        if request:
            for item in request:
                tmp_dict = {'id': item['objectid'],
                            'name': item.text,
                            }
                info_dict[key].append(tmp_dict)
        info_dict[key] = sorted(info_dict[key], key=lambda category: category['name'])


# обновление статистических параметров
def update_statistic_data(game, info_dict):
    stat_keys = ['rank',
                 'usersrated',
                 'average',
                 'bayesaverage',
                 ]
    ranks = game.find_all('rank')
    for rank in ranks:
        if rank['name'] == 'boardgame':
            info_dict['rank'].append(rank['value'])
    for key in stat_keys[1:]:
        info_dict[key].append(game.find(key).text)


time_start = datetime.datetime.now()
url_bgg_start = "https://boardgamegeek.com/browse/boardgame/page/"
url_go = "https://godville.net/stats/guild/%D0%A7%D0%B5%D1%88%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D0%94%D0%BE%D0%BC"
driver_path = r"C:\chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome(driver_path)

page_num = 1
driver.get(url_bgg_start + str(page_num))
all_pages = driver.find_element_by_class_name("fr")
fin_page = int(all_pages.text[-5:-1])

games_data = {}
while page_num <= fin_page:
    driver.get(url_bgg_start + str(page_num))
    trs = driver.find_elements_by_class_name("collection_objectname")
    ids = []
    for _ in trs:
        link = _.find_element_by_tag_name("a").get_attribute("href")
        ids.append(get_obj_id(link))
    all_ids = ",".join(ids)
    api_url = f'https://www.boardgamegeek.com/xmlapi/boardgame/{all_ids}?stats=1'
    for game_id in ids:
        games_data[game_id] = {
            'rank': [],
            'title': [],
            'other_titles': [],
            'thumbnail': [],
            'image': [],
            'usersrated': [],
            'average': [],
            'bayesaverage': [],
            'yearpublished': [],
            'minplayers': [],
            'maxplayers': [],
            'minplaytime': [],
            'maxplaytime': [],
            'age': [],
            'description': [],
            'boardgamedesigner': [],
            'boardgameartist': [],
            'boardgamepublisher': [],
            'boardgamecategory': [],
            'boardgamemechanic': [],
            'boardgamefamily': [],
            'boardgamesubdomain': [],
            'boardgameexpansion': [],
            'boardgameintegration': [],
            'boardgamepodcastepisode': [],
            'boardgamehonor': [],
            'boardgameversion': [],
            'boardgameaccessory': [],
        }
    soup_for_games = get_soup_lxml(api_url)
    boardgames = soup_for_games.find_all('boardgame')
    for boardgame in boardgames:
        cur_id = boardgame['objectid']
        update_boardgame_titles(boardgame, games_data[cur_id])
        update_boardgame_ess_wo_ids(boardgame, games_data[cur_id])
        update_boardgame_ess_with_ids(boardgame, games_data[cur_id])
        update_boardgame_not_ess_with_ids(boardgame, games_data[cur_id])
        update_statistic_data(boardgame, games_data[cur_id])
    page_num += 1

driver.close()
