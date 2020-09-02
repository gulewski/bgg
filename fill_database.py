import creds
import db_entities as dbt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from requests.exceptions import ConnectionError
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
    pure_join_conns = {"boardgameaccessory": ("accessories", "bgames_accessories"),
                       "boardgameartist": ("artists", "bgames_artists"),
                       "boardgamecategory": ("categories", "bgames_categories"),
                       "boardgamedesigner": ("designers", "bgames_designers"),
                       "boardgameexpansion": ("expansions", "bgames_expansions"),
                       "boardgamefamily": ("families", "bgames_families"),
                       "boardgamehonor": ("honors", "bgames_honors"),
                       "boardgameintegration": ("integrations", "bgames_integrations"),
                       "boardgamemechanic": ("mechanics", "bgames_mechanics"),
                       "boardgamepodcastepisode": ("podcasts", "bgames_podcasts"),
                       "boardgamepublisher": ("publishers", "bgames_publishers"),
                       "boardgamesubdomain": ("subdomains", "bgames_subdomains"),
                       "boardgameversion": ("versions", "bgames_versions"),
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
                    try:
                        current_bgame[tag.name] = float(tag.text)
                    except ValueError:
                        current_bgame[tag.name] = 0.0
                elif tag.name in ["image", "thumbnail"]:  # text fields
                    current_bgame[tag.name] = tag.text
                else:  # int fields
                    try:
                        current_bgame[tag.name] = int(tag.text)
                    except ValueError:
                        pass
            elif tag.name in pure_join_conns.keys():
                bgames_dataset[pure_join_conns[tag.name][0]].add((tag["objectid"],
                                                                  tag.text))
                bgames_dataset[pure_join_conns[tag.name][1]].add((current_objectid,
                                                                  tag["objectid"]))
    bgames_dataset["bgames"].append(current_bgame)


def gather_data(start_page: int, final_page: int, dataset: dict):
    current_page = start_page
    try:
        for page in range(start_page, final_page):
            # checking time for ban avoiding
            time_loop = time.time()
            # getting list of bg ids for current page
            id_list, descriptions = get_ids_and_descriptions(creds.BGG_BROWSE_PAGE, page)
            # creating URI for xmlapi request
            xmlapi_ref = creds.XMLAPI_START + ",".join(id_list) + creds.XMLAPI_END
            print(xmlapi_ref)
            # get xmlapi page itself and put it in soup-object
            xmlapi_page = requests.get(xmlapi_ref)
            soup_for_games = BeautifulSoup(xmlapi_page.text, features="lxml")
            # creating a list of boardgames for current xmlapi page
            boardgames = soup_for_games.find_all("boardgame")
            # updating dataset for each boardgame on the page
            for boardgame in boardgames:
                try:
                    if boardgame["inbound"]:
                        continue
                except KeyError:
                    update_dataset(descriptions, dataset, boardgame)
            print(f"page #{page}\n"
                  f"accessories: {len(dataset['accessories'])}, {len(dataset['bgames_accessories'])}\n"
                  f"artists: {len(dataset['artists'])}, {len(dataset['bgames_artists'])}\n"
                  f"categories: {len(dataset['categories'])}, {len(dataset['bgames_categories'])}\n"
                  f"designers: {len(dataset['designers'])}, {len(dataset['bgames_designers'])}\n"
                  f"expansions: {len(dataset['expansions'])}, {len(dataset['bgames_expansions'])}\n"
                  f"families: {len(dataset['families'])}, {len(dataset['bgames_families'])}\n"
                  f"honors: {len(dataset['honors'])}, {len(dataset['bgames_honors'])}\n"
                  f"integrations: {len(dataset['integrations'])}, {len(dataset['bgames_integrations'])}\n"
                  f"mechanics: {len(dataset['mechanics'])}, {len(dataset['bgames_mechanics'])}\n"
                  f"podcasts: {len(dataset['podcasts'])}, {len(dataset['bgames_podcasts'])}\n"
                  f"publishers: {len(dataset['publishers'])}, {len(dataset['bgames_publishers'])}\n"
                  f"subdomains: {len(dataset['subdomains'])}, {len(dataset['bgames_subdomains'])}\n"
                  f"versions: {len(dataset['versions'])}, {len(dataset['bgames_versions'])}\n"
                  f"bgames: {len(dataset['bgames'])}")
            if time.time() - time_loop < 3:
                time.sleep(3)
            current_page = page + 1
            print(datetime.datetime.now() - time_start)
    except ConnectionError:
        print("got ConnectionError")
        gather_data(current_page, final_page, dataset)


# start of work
time_start = datetime.datetime.now()

start = 1
finish = get_final_page(creds.BGG_BROWSE_PAGE + "1") + 1

data = {"bgames": list(),
        "accessories": set(),
        "artists": set(),
        "categories": set(),
        "designers": set(),
        "expansions": set(),
        "families": set(),
        "honors": set(),
        "integrations": set(),
        "mechanics": set(),
        "podcasts": set(),
        "publishers": set(),
        "subdomains": set(),
        "versions": set(),
        "bgames_accessories": set(),
        "bgames_artists": set(),
        "bgames_categories": set(),
        "bgames_designers": set(),
        "bgames_expansions": set(),
        "bgames_families": set(),
        "bgames_honors": set(),
        "bgames_integrations": set(),
        "bgames_mechanics": set(),
        "bgames_podcasts": set(),
        "bgames_publishers": set(),
        "bgames_subdomains": set(),
        "bgames_versions": set(),
        }

gather_data(start, finish, data)

print("writing file")
with open('data.txt', 'w') as file:
    file.write(str(data))

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
