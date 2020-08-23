import creds
import db_entities as dbt

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup

import datetime


# creating session to database
def create_db_session():
    engine = create_engine(creds.SQLALCHEMY_DATABASE_URI)
    dbt.Base.metadata.create_all(engine)
    output_session = sessionmaker(bind=engine)()
    return output_session


# getting final page of boardgamegeek/browse link
def get_final_page(active_driver):
    active_driver.get(creds.BGG_BROWSE_PAGE + "1")
    all_pages = active_driver.find_element_by_class_name("fr").text
    result = all_pages[all_pages.find("[") + 1:all_pages.find("]")]
    return int(result)


# collecting all ids from current page
def get_ids_list(active_driver, page_num: int):
    # collecting game id from link
    def get_obj_id(link: str):
        word_list = link.split("/")
        for _ in word_list:
            if _.isdigit():
                return _
        return None

    # in progress
    def get_description():
        pass

    active_driver.get(creds.BGG_BROWSE_PAGE + str(page_num))
    table_rows = active_driver.find_elements_by_class_name("collection_objectname")
    id_list = []
    descriptions = {}
    # if you like comprehensions, uncomment this
    # id_list = [get_obj_id(row.find_element_by_tag_name("a").get_attribute("href")) for row in table_rows]
    for row in table_rows:
        game_link = row.find_element_by_tag_name("a").get_attribute("href")
        id = get_obj_id(game_link)
        id_list.append(id)
        # in progress
        descriptions[id] = get_description()
    return id_list


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


# in progress
# updating sublist for boardgames itself
# remember to take description out of table
def update_bgames(bgames_table: list):
    pass

# start of work
time_start = datetime.datetime.now()
driver = webdriver.Chrome(creds.WEBDRIVER_PATH)

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

for page in range(1, 2):  # get_final_page(driver)+1):
    # entities for people and connections with boardgdames
    people, bgames_people = [], []
    # entities for tags and connections with boardgdames
    tags, bgames_tags = [], []
    # entities for additionals and connections with boardgdames
    additionals, bgames_additionals = [], []
    # entities for related games and connections with boardgdames
    related, bgames_related = [], []
    # getting list of bg ids for current page
    id_list = get_ids_list(driver, page)
    # creating URI for xmlapi request
    xmlapi_ref = creds.XMLAPI_START + ",".join(id_list) + creds.XMLAPI_END
    # get xmlapi page itself and put it in soup-object
    xmlapi_page = requests.get(xmlapi_ref)
    soup_for_games = BeautifulSoup(xmlapi_page.text, features="lxml")
    # creating a list of boardgames for current xmlapi page
    boardgames = soup_for_games.find_all('boardgame')
    # for each boardgame updating sublists of entities
    for boardgame in boardgames[:5]:
        update_sublists(people_type_link_conn, people, bgames_people, boardgame)
        update_sublists(tags_type_link_conn, tags, bgames_tags, boardgame)
        update_sublists(additionals_type_link_conn, additionals, bgames_additionals, boardgame)
        update_sublists(related_type_link_conn, related, bgames_related, boardgame)
    print(f"people: {len(people)}, {len(set(people))}, {len(bgames_people)}\n"
          f"tags: {len(tags)}, {len(set(tags))}, {len(bgames_tags)}\n"
          f"additionals: {len(additionals)}, {len(set(additionals))}, {len(bgames_additionals)}\n"
          f"related: {len(related)}, {len(set(related))}, {len(bgames_related)}\n"
          f"{bgames_related[:3]}")
    #
    # for game_id in id_list:
    #     games_data[game_id] = {
    #         # bgame
    #         'rank': [],
    #         'title': [],
    #         'thumbnail': [],
    #         'image': [],
    #         'usersrated': [],
    #         'average': [],
    #         'bayesaverage': [],
    #         'yearpublished': [],
    #         'minplayers': [],
    #         'maxplayers': [],
    #         'playtime': [],
    #         'minplaytime': [],
    #         'maxplaytime': [],
    #         'age': [],
    #         'description': [],
    #         # people
    #         'boardgamedesigner': [],
    #         'boardgameartist': [],
    #         'boardgamepublisher': [],
    #         # tags
    #         'boardgamecategory': [],
    #         'boardgamemechanic': [],
    #         'boardgamefamily': [],
    #         'boardgamesubdomain': [],
    #         # related games
    #         'boardgameexpansion': [],
    #         'boardgameintegration': [],
    #         # additionals
    #         'boardgamepodcastepisode': [],
    #         'boardgamehonor': [],
    #         'boardgameversion': [],
    #         'boardgameaccessory': [],
    #         'other_titles': [],
    #     }

# 1 запрашиваем номер финальной страницы с бгг
# 2 в цикле от 1 до финальной страницы вкл-но собираем со страницы ID игр
# 3 запрашиваем по кадой странице xmlapi с сотней игр (кроме последней страницы)
# 4 разбираем апишку в словарь
# 5 вносим из словар все по таблицам базы данны
# 6 профит

driver.close()
print(datetime.datetime.now() - time_start)


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
