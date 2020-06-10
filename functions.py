import requests
from bs4 import BeautifulSoup


# на будущее. создание списка урлов по количеству игр и с сортировкой
def create_url_list(num_games: int, sort: str = 'rank', sortdir: str ='asc'):
    # sort in ['rank', 'title', 'bggrating', 'avgrating', 'numvoters'],
    # sortdir in ['asc', 'desc']
    i, urls = 1, []
    while num_games > 0:
        num_games -= 100
        urls.append(f'https://boardgamegeek.com/browse/boardgame/page/{i}?sort={sort}&sortdir={sortdir}')
        i += 1
    return urls


# получить html-soup-объект по url
def get_soup_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, features='html.parser')


# получить lxml-soup-объект по url
def get_soup_lxml(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, features='lxml')


# получение таблицы с играми по soup-объекту. в полной таблице 100 игр
def get_game_table(soup):
    return soup.find('div', {'class': 'table-responsive'}).find_all('tr')[1:]


# получение рейтингов игры и количества проголосовавших
def get_ratings_and_numvoters(game):
    all_ratings = [i.text.strip() for i in game.find_all('td', {'class': 'collection_bggrating'})]
    bgg_rating = [all_ratings[0]]
    avg_rating = [all_ratings[1]]
    num_voters = [all_ratings[2]]
    return bgg_rating, avg_rating, num_voters


# получение objectid игры для запросов к API
def get_objectid(game):
    objid = game.find('td', {'class': 'collection_thumbnail'}).a['href'][1:]
    objid = objid[objid.find('/') + 1:]
    return objid[:objid.find('/')]


# функция, собирающая стартовую инфу по игре
def collect_game_initial_info(game, info_dict, oid_list):
    game_oid = get_objectid(game)
    game_bggrating, game_avgrating, game_numvoters = get_ratings_and_numvoters(game)
    info_dict[game_oid] = {}
    info_dict[game_oid]['rank'] = [game.find('td', {'class': 'collection_rank'}).text.strip()]
    info_dict[game_oid]['title'] = [game.find('td', {'class': 'collection_objectname'}).a.text.strip()]
    info_dict[game_oid]['bggrating'] = game_bggrating
    info_dict[game_oid]['avgrating'] = game_avgrating
    info_dict[game_oid]['numvoters'] = game_numvoters
    oid_list.append(game_oid)
    return info_dict, oid_list


# получаем словарь со всеми тегами и значениями по игре
def get_api_boardgame_dict(boardgame):
    bg_dict = {}
    for child in boardgame.children:
        if child.name:
            try:
                bg_dict[child.name].append(child.text)
            except KeyError:
                bg_dict[child.name] = [child.text]
    essential_keys = ['yearpublished', 'minplayers', 'maxplayers', 'minplaytime', 'maxplaytime', 'age',
                      'boardgamedesigner', 'boardgameartist', 'boardgamepublisher',
                      'boardgamesubdomain', 'boardgamecategory', 'boardgamemechanic', 'boardgamefamily',
                      'boardgameexpansion', 'boardgameintegration']
    key_for_delete = [key for key in bg_dict.keys() if key not in essential_keys]
    for key in key_for_delete:
        bg_dict.pop(key)
    return bg_dict


# функция, собирающая расширенную инфу по игре
def collect_game_extended_info(oids, info_dict):
    all_oids = ','.join(oids)
    api_url = f'https://www.boardgamegeek.com/xmlapi/boardgame/{all_oids}'
    soup = get_soup_lxml(api_url)
    all_bg = soup.find_all('boardgame', inbound=False)
    for boardgame in all_bg:
        bg_dict = get_api_boardgame_dict(boardgame)
        info_dict[boardgame['objectid']].update(bg_dict)
    return info_dict
