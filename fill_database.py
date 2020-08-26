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


def update_dataset(descs: dict, bgames_dataset: dict, bgame):
    bgames_structure = {"objectid": None,
                        "name": None,
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
    additionals_type_link_conn = {"boardgameversion": "version",
                                  "boardgamehonor": "honor",
                                  "boardgamepodcastepisode": "podcast",
                                  "boardgameaccessory": "accessory",
                                  }
    people_type_link_conn = {"boardgamedesigner": "designer",
                             "boardgameartist": "artist",
                             "boardgamepublisher": "publisher",
                             }
    related_type_link_conn = {"boardgameintegration": "integration",
                              "boardgameexpansion": "expansion",
                              }
    tags_type_link_conn = {"boardgamecategory": "category",
                           "boardgamemechanic": "mechanic",
                           "boardgamefamily": "family",
                           "boardgamesubdomain": "subdomain",
                           }
    current_objectid = bgame["objectid"]
    current_bgame = bgames_structure.copy()
    current_taglist = bgame.find_all()
    current_bgame["objectid"] = int(current_objectid)  # special case with objectid
    for tag in current_taglist:
        try:
            if tag["inbound"]:
                continue
        except KeyError:
            if tag.name in current_bgame.keys():  # updating boardgame fields
                if tag.name == "description":  # gathered from page
                    current_bgame[tag.name] = descs[current_objectid]
                elif tag.name == "name":  # special case with name
                    try:
                        if tag["primary"] == "true":
                            current_bgame[tag.name] = tag.text
                    except KeyError:
                        pass
                elif tag.name == "rank":  # special case with rank
                    if tag["name"] == "boardgame":
                        try:
                            current_bgame[tag.name] = int(tag["value"])
                        except ValueError:
                            pass
                elif tag.name in ["average", "bayesaverage"]:  # float fields
                    current_bgame[tag.name] = float(tag.text)
                elif tag.name in ["image", "thumbnail"]:  # text fields
                    current_bgame[tag.name] = tag.text
                else:  # int fields
                    try:
                        current_bgame[tag.name] = int(tag.text)
                    except ValueError:
                        pass
            elif tag.name in additionals_type_link_conn.keys():
                bgames_dataset["additionals"].add((tag['objectid'],
                                                   tag.text))
                bgames_dataset["bgames_additionals"].add((boardgame['objectid'],
                                                          tag['objectid'],
                                                          additionals_type_link_conn[tag.name],
                                                          tag.name))
            elif tag.name in people_type_link_conn.keys():
                bgames_dataset["people"].add((tag['objectid'],
                                              tag.text))
                bgames_dataset["bgames_people"].add((boardgame['objectid'],
                                                     tag['objectid'],
                                                     people_type_link_conn[tag.name],
                                                     tag.name))
            elif tag.name in related_type_link_conn.keys():
                bgames_dataset["related_games"].add((tag['objectid'],
                                                     tag.text))
                if tag.name == "boardgameintegration":  # special case for integrations
                    bgames_dataset["bgames_related_games"].add((boardgame['objectid'],
                                                                tag['objectid'],
                                                                related_type_link_conn[tag.name],
                                                                "boardgame"))
                else:
                    bgames_dataset["bgames_related_games"].add((boardgame['objectid'],
                                                                tag['objectid'],
                                                                related_type_link_conn[tag.name],
                                                                tag.name))
            elif tag.name in tags_type_link_conn.keys():
                bgames_dataset["tags"].add((tag['objectid'],
                                            tag.text))
                bgames_dataset["bgames_tags"].add((boardgame['objectid'],
                                                   tag['objectid'],
                                                   tags_type_link_conn[tag.name],
                                                   tag.name))
    bgames_dataset["bgames"].append(current_bgame)


# start of work
time_start = datetime.datetime.now()

final_page = get_final_page(creds.BGG_BROWSE_PAGE + "1") + 1

for page in range(1, 3):
    current_loop_time = datetime.datetime.now()
    # getting list of bg ids for current page
    id_list, descriptions = get_ids_and_descriptions(creds.BGG_BROWSE_PAGE, page)
    # creating URI for xmlapi request
    xmlapi_ref = creds.XMLAPI_START + ",".join(id_list) + creds.XMLAPI_END
    # get xmlapi page itself and put it in soup-object
    print(xmlapi_ref)
    xmlapi_page = requests.get(xmlapi_ref)
    soup_for_games = BeautifulSoup(xmlapi_page.text, features="lxml")
    # creating a list of boardgames for current xmlapi page
    boardgames = soup_for_games.find_all('boardgame')
    # creating a dataset for game data
    data = {"bgames": list(),
            "additionals": set(),
            "bgames_additionals": set(),
            "people": set(),
            "bgames_people": set(),
            "related_games": set(),
            "bgames_related_games": set(),
            "tags": set(),
            "bgames_tags": set(),
            }
    # updating dataset for each boardgame on the page
    for boardgame in boardgames:
        try:
            if boardgame["inbound"]:
                continue
        except KeyError:
            update_dataset(descriptions, data, boardgame)
    print(f"page #{page}\n"
          f"people: {len(data['people'])}, {len(data['bgames_people'])}\n"
          f"tags: {len(data['tags'])}, {len(data['bgames_tags'])}\n"
          f"additionals: {len(data['additionals'])}, {len(data['bgames_additionals'])}\n"
          f"related: {len(data['related_games'])}, {len(data['bgames_related_games'])}\n"
          f"bgames: {len(data['bgames'])}")
    print(data["bgames"])
    if datetime.datetime.now() - current_loop_time > datetime.timedelta(3):
        continue
    else:
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
