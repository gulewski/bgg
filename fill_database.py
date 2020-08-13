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

    active_driver.get(creds.BGG_BROWSE_PAGE + str(page_num))
    table_rows = active_driver.find_elements_by_class_name("collection_objectname")
    id_list = []
    # if you like comprehensions, uncomment this
    # id_list = [get_obj_id(row.find_element_by_tag_name("a").get_attribute("href")) for row in table_rows]
    for row in table_rows:
        game_link = row.find_element_by_tag_name("a").get_attribute("href")
        id_list.append(get_obj_id(game_link))
    return id_list


# in progress
def create_dictionary_people(bg):
    type_link_conn = {"boardgamedesigner": "designer",
                      "boardgameartist": "artist",
                      "boardgamepublisher": "publisher",
                      }
    designers = bg.find_all("boardgamedesigner")
    designers_dict = {}
    for _ in designers:
        designers_dict[_["objectid"]]= _.text
    artists = bg.find_all("boardgameartist")
    artists_dict = {}
    for _ in artists:
        artists_dict[_["objectid"]] = _.text
    publishers = bg.find_all("boardgamepublisher")
    publishers_dict = {}
    for _ in publishers:
        artists_dict[_["objectid"]] = _.text
    print(designers_dict, artists_dict, publishers_dict)
    pass

# start of work
time_start = datetime.datetime.now()
driver = webdriver.Chrome(creds.WEBDRIVER_PATH)

for page in range(1, 2):  # get_final_page(driver)+1):
    games_data = {}
    id_list = get_ids_list(driver, page)
    xmlapi_ref = creds.XMLAPI_START + ",".join(id_list) + creds.XMLAPI_END
    xmlapi_page = requests.get(xmlapi_ref)
    soup_for_games = BeautifulSoup(xmlapi_page.text, features="lxml")
    boardgames = soup_for_games.find_all('boardgame')
    for boardgame in boardgames:
        create_dictionary_people(boardgame)
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
