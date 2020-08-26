import creds
import db_entities as dbt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import urllib3  # will be used for search function
from bs4 import BeautifulSoup

import time
import datetime
import json


# creating session to database
def create_db_session():
    engine = create_engine(creds.SQLALCHEMY_DATABASE_URI)
    dbt.Base.metadata.create_all(engine)
    output_session = sessionmaker(bind=engine)()
    return output_session


# getting final page of boardgamegeek/browse link
def get_final_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    pages = soup.find("div", {"class": "fr"}).text
    result = pages[pages.find("[") + 1:pages.find("]")]
    return int(result)


# collecting all ids and descriptions from current page
def get_ids_and_descriptions(url_base, page_num: int):
    # collecting game id from row
    def get_obj_id(game_row):
        link = game_row.find("a", {"class": "primary"})["href"]
        word_list = link.split("/")
        for word in word_list:
            if word.isdigit():
                return word
        return None

    # collecting game descriptions from row
    def get_description(game_row):
        try:
            return game_row.find("p").text.strip()
        except AttributeError:
            return None

    response = requests.get(url_base + str(page_num))
    soup = BeautifulSoup(response.text, features="html.parser")
    table_rows = soup.find("div", {"class": "table-responsive"}).find_all("tr")[1:]
    ids_list = []
    descs = {}
    for row in table_rows:
        cur_id = get_obj_id(row)
        ids_list.append(cur_id)
        descs[cur_id] = get_description(row)
    return ids_list, descs


# updating sublists for core tables and connection between core table and boardgames table
def update_sublists(conn_keys: dict, pure_table: list, bg_conn_table: list, bg):
    for tag in conn_keys.keys():
        type_searching = bg.find_all(tag)
        for element in type_searching:
            try:
                if element["inbound"]:
                    continue
            except KeyError:
                pure_table.append(tuple((element["objectid"], element.text)))
                # a crutch for integrations
                if tag == "boardgameintegration":
                    bg_conn_table.append(tuple((bg["objectid"], element["objectid"], conn_keys[tag], "boardgame")))
                else:
                    bg_conn_table.append(tuple((bg["objectid"], element["objectid"], conn_keys[tag], tag)))


# updating sublist for boardgames itself
def update_bgames(dict_with_descs: dict, bgames_table: dict, template, bg):
    current_id = bg["objectid"]
    current_bgame = template.copy()
    for key in current_bgame.keys():
        if key == 'description':  # gathered from page
            current_bgame['description'] = dict_with_descs[current_id]
        elif key == "name":  # special case with name
            all_names = bg.find_all("name")
            for name in all_names:
                try:
                    if name["primary"] == "true":
                        current_bgame["name"] = name.text
                        continue
                except KeyError:
                    pass
        elif key in ["image",
                     "thumbnail",
                     ]:  # varchar fields
            try:
                current_bgame[key] = bg.find(key).text
            except AttributeError:
                pass
        elif key in ["yearpublished",
                     "minplayers",
                     "maxplayers",
                     "playingtime",
                     "minplaytime",
                     "maxplaytime",
                     "age",
                     ]:  # int not statistics fields
            try:
                current_bgame[key] = int(bg.find(key).text)
            except AttributeError:
                pass
            except ValueError:
                pass
        else:  # statistics
            if key == "rank":  # special case with rank
                all_ranks = bg.find_all("rank")
                for rank in all_ranks:
                    if rank["name"] == "boardgame":
                        try:
                            current_bgame[key] = int(rank["value"])
                        except ValueError:
                            pass
            elif key == "usersrated":  # int statistic field
                try:
                    current_bgame[key] = int(bg.find(key).text)
                except AttributeError:
                    pass
            else:  # float ranks
                try:
                    current_bgame[key] = float(bg.find(key).text)
                except AttributeError:
                    pass
    bgames_table[current_id] = current_bgame


# start of work
time_start = datetime.datetime.now()

people_type_link_conn = {"boardgamedesigner": "designer",
                         "boardgameartist": "artist",
                         "boardgamepublisher": "publisher",
                         }
tags_type_link_conn = {"boardgamecategory": "category",
                       "boardgamemechanic": "mechanic",
                       "boardgamefamily": "family",
                       "boardgamesubdomain": "subdomain",
                       }
additionals_type_link_conn = {"boardgameversion": "version",
                              "boardgamehonor": "honor",
                              "boardgamepodcastepisode": "podcast",
                              "boardgameaccessory": "accessory",
                              }
related_type_link_conn = {"boardgameintegration": "integration",
                          "boardgameexpansion": "expansion",
                          }
bgames_template = {"name": None,
                   "yearpublished": None,
                   "minplayers": None,
                   "maxplayers": None,
                   "playingtime": None,
                   "minplaytime": None,
                   "maxplaytime": None,
                   "age": None,
                   "thumbnail": None,
                   "image": None,
                   "description": None,
                   "rank": None,
                   "usersrated": None,
                   "average": None,
                   "bayesaverage": None,
                   }

final_page = get_final_page(creds.BGG_BROWSE_PAGE + "1") + 1

for page in range(1, 2):
    # getting list of bg ids for current page
    id_list, descriptions = get_ids_and_descriptions(creds.BGG_BROWSE_PAGE, page)
    # creating URI for xmlapi request
    xmlapi_ref = creds.XMLAPI_START + ",".join(id_list) + creds.XMLAPI_END
    print(xmlapi_ref)
    # get xmlapi page itself and put it in soup-object
    xmlapi_page = requests.get(xmlapi_ref)
    soup_for_games = BeautifulSoup(xmlapi_page.text, features="lxml")
    # creating a list of boardgames for current xmlapi page
    boardgames = soup_for_games.find_all('boardgame')
    # entity for boardgame itself
    bgames = {}
    # entities for people and connections with boardgdames
    people, bgames_people = [], []
    # entities for tags and connections with boardgdames
    tags, bgames_tags = [], []
    # entities for additionals and connections with boardgdames
    additionals, bgames_additionals = [], []
    # entities for related games and connections with boardgdames
    related, bgames_related = [], []
    # for each boardgame updating sublists of entities
    for boardgame in boardgames:
        try:
            if boardgame["inbound"]:
                continue
        except KeyError:
            update_sublists(people_type_link_conn, people, bgames_people, boardgame)
            update_sublists(tags_type_link_conn, tags, bgames_tags, boardgame)
            update_sublists(additionals_type_link_conn, additionals, bgames_additionals, boardgame)
            update_sublists(related_type_link_conn, related, bgames_related, boardgame)
            update_bgames(descriptions, bgames, bgames_template, boardgame)

    print(f"page #{page}\n"
          f"people: {len(people)}, {len(set(people))}, {len(bgames_people)}\n"
          f"tags: {len(tags)}, {len(set(tags))}, {len(bgames_tags)}\n"
          f"additionals: {len(additionals)}, {len(set(additionals))}, {len(bgames_additionals)}\n"
          f"related: {len(related)}, {len(set(related))}, {len(bgames_related)}\n"
          f"bgames: {len(bgames)}")
    # add sleeper to avoid bggAPI ban :)
    time.sleep(3)

# + 1 запрашиваем номер финальной страницы с бгг
# + 2 в цикле от 1 до финальной страницы вкл-но собираем со страницы ID игр и описания
# + 3 запрашиваем по кадой странице xmlapi с сотней игр (кроме последней страницы)
# + 4 разбираем апишку в словарь
# 5 вносим из словар все по таблицам базы данны
# 6 профит

print(f"spent {datetime.datetime.now() - time_start}")


# cleaning all tables in database
def delete_all_data():
    session = create_db_session()
    table_list = [dbt.Additionals,
                  dbt.Bgames,
                  dbt.BgamesAdditionals,
                  dbt.BgamesPeople,
                  dbt.BgamesRelatedGames,
                  dbt.BgamesTags,
                  dbt.People,
                  dbt.RelatedGames,
                  dbt.Tags,
                  ]
    for table in table_list:
        query = session.query(table)
        query.delete()
    session.commit()
    session.close()
