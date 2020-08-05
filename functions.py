import requests
import lxml
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
        info_dict['usersrated'].append(game.find('usersrated').text)
        info_dict['average'].append(game.find('average').text)
        info_dict['bayesaverage'].append(game.find('bayesaverage').text)

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
            'rank': [],
            'title': [],
            # 'alt_titles': [],
            'thumbnail': [],
            # 'image': [],
            'usersrated': [],
            'average': [],
            'bayesaverage': [],
            'yearpublished': [],
            'minplayers': [],
            'maxplayers': [],
            'minplaytime': [],
            'maxplaytime': [],
            'age': [],
            # 'description': [],

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
            # 'videogamebg': [],
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

    # print(json.dumps(games_data, indent=2, ensure_ascii=False))
    return games_data
