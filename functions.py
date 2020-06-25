import requests
import json
from bs4 import BeautifulSoup


def get_games_info(
        quantity_games: int = None,
        sort_by: str = 'rank',
        sort_dir: str = 'asc',
        search_string: str = None,
        exact: int = 0, ):
    # создание списка урлов по количеству игр и с сортировкой
    def create_url_list(
            num_games: int,
            sort_param: str = 'rank',
            sort_direction: str = 'asc', ):
        # sort_param in ['rank', 'title', 'bggrating', 'avgrating', 'numvoters'],
        # sort_direction in ['asc', 'desc']
        counter, urls = 1, []
        while num_games > 0:
            num_games -= 100
            urls.append(f'https://boardgamegeek.com/browse/boardgame/'
                        f'page/{counter}'
                        f'?sort={sort_param}&sortdir={sort_direction}')
            counter += 1
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

    # получение object_id игры для запросов к API
    def get_object_id_from_table(game):
        obj_id = game.find('td', {'class': 'collection_thumbnail'}).a['href'][1:]
        obj_id = obj_id[obj_id.find('/') + 1:]
        return obj_id[:obj_id.find('/')]

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
        # info_dict['alt_titles'] = other_names

    # обновление списков ключей без objectid
    def update_boardgame_ess_wo_ids(game, info_dict):
        ess_keys_wo_oid = ['yearpublished',
                           'minplayers',
                           'maxplayers',
                           'minplaytime',
                           'maxplaytime',
                           'age',
                           'thumbnail',
                           # 'image',
                           # 'description',
                           ]
        for key in ess_keys_wo_oid:
            info_dict[key] = []
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
            info_dict[key] = []
            request = game.find_all(key)
            if request:
                for item in request:
                    tmp_dict = {'id': item['objectid'],
                                'name': item.text,
                                }
                    info_dict[key].append(tmp_dict)

    # обновление неважных списков ключей с objectid
    def update_boardgame_not_ess_with_ids(game, info_dict):
        not_ess_keys_with_oid = ['boardgamehonor',
                                 'boardgamepodcastepisode',
                                 'boardgameversion',
                                 # 'videogamebg',
                                 'boardgameaccessory',
                                 ]
        for key in not_ess_keys_with_oid:
            info_dict[key] = []
            request = game.find_all(key)
            if request:
                for item in request:
                    tmp_dict = {'id': item['objectid'],
                                'name': item.text,
                                }
                    info_dict[key].append(tmp_dict)

    # создание url-строки с objectid игр для запроса в api,
    # независимо от того, получены они через поиск или через сортировку.
    # если список пустой, функция возвращает False
    object_ids = []
    if quantity_games:
        url_list = create_url_list(quantity_games, sort_by, sort_dir)
        url_number = 0
        while quantity_games > 0:
            if quantity_games // 100 >= 1:
                end_pos = None
            else:
                end_pos = quantity_games % 100
            quantity_games -= 100

            cur_url = url_list[url_number]
            cur_games_table = get_game_table(get_soup_html(cur_url))
            url_number += 1
            for cur_game in cur_games_table[0:end_pos]:
                object_ids.append(get_object_id_from_table(cur_game))
    elif search_string:
        search_url = f'https://www.boardgamegeek.com/xmlapi' \
                     f'/search?search={search_string}&exact={exact}'
        soup_for_ids = get_soup_lxml(search_url)
        for boardgame in soup_for_ids.find_all('boardgame'):
            object_ids.append(boardgame['objectid'])
    else:
        return False
    if object_ids:
        object_ids_string = ','.join(object_ids)
        api_url = f'https://www.boardgamegeek.com/xmlapi/' \
                  f'boardgame/{object_ids_string}?stats=1'
    else:
        return False

    # создание словаря-шаблона для данных по играм
    games_data = {}
    for game_id in object_ids:
        games_data[game_id] = {
            'title': None,
            # 'alt_titles': None,
            'thumbnail': None,
            # 'image': None,
            'yearpublished': None,
            'minplayers': None,
            'maxplayers': None,
            'minplaytime': None,
            'maxplaytime': None,
            'age': None,
            # 'description': None,

            'boardgamedesigner': None,
            'boardgameartist': None,
            'boardgamepublisher': None,
            'boardgamecategory': None,
            'boardgamemechanic': None,
            'boardgamefamily': None,
            'boardgamesubdomain': None,
            'boardgameexpansion': None,
            'boardgameintegration': None,

            'boardgamepodcastepisode': None,
            'boardgamehonor': None,
            'boardgameversion': None,
            # 'videogamebg': None,
            'boardgameaccessory': None,
        }

    soup_for_games = get_soup_lxml(api_url)
    boardgames = soup_for_games.find_all('boardgame')
    for boardgame in boardgames:
        cur_id = boardgame['objectid']
        update_boardgame_titles(boardgame, games_data[cur_id])
        update_boardgame_ess_wo_ids(boardgame, games_data[cur_id])
        update_boardgame_ess_with_ids(boardgame, games_data[cur_id])
        update_boardgame_not_ess_with_ids(boardgame, games_data[cur_id])

    #print(json.dumps(games_data, indent=2, ensure_ascii=False))
    return games_data


def get_dict_with_all_games(num_games: int = None, sort: str = 'rank', sortdir: str = 'asc'):
    # создание списка урлов по количеству игр и с сортировкой
    def create_url_list(num_games: int, sort: str = 'rank', sortdir: str = 'asc'):
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
        essential_keys = ['yearpublished', 'minplayers', 'maxplayers', 'minplaytime', 'maxplaytime', 'age',
                          'boardgamedesigner', 'boardgameartist', 'boardgamepublisher',
                          'boardgamesubdomain', 'boardgamecategory', 'boardgamemechanic', 'boardgamefamily',
                          'boardgameexpansion', 'boardgameintegration']
        for key in essential_keys:
            bg_dict.setdefault(key, ['N/A'])
        for child in boardgame.children:
            if child.name:
                try:
                    if bg_dict[child.name] == ['N/A']:
                        bg_dict[child.name] = [child.text]
                    else:
                        bg_dict[child.name].append(child.text)
                except KeyError:
                    pass
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

    url_list = create_url_list(num_games, sort, sortdir)
    fin_dict, i = {}, 0
    while num_games > 0:
        cur_dict = {}
        oids = []
        if num_games // 100 >= 1:
            end_pos = None
        else:
            end_pos = num_games % 100
        num_games -= 100

        url = url_list[i]
        cur_games_table = get_game_table(get_soup_html(url))
        i += 1
        for cur_game in cur_games_table[0:end_pos]:
            cur_dict, oids = collect_game_initial_info(cur_game, cur_dict, oids)
        cur_dict = collect_game_extended_info(oids, cur_dict)
        fin_dict.update(cur_dict)

    return fin_dict
