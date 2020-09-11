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
                       "boardgameartist": None,
                       "boardgamecategory": ("categories", "bgames_categories"),
                       "boardgamedesigner": None,
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
                if tag.name in ("boardgameartist", "boardgamedesigner"):  # special case with people
                    bgames_dataset["people"].add((tag["objectid"],
                                                  tag.text))
                    bgames_dataset["bgames_people"].add((current_objectid,
                                                         tag["objectid"],
                                                         tag.name))
                else:
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
            print(f"page #{page}/{final_page-1}\n"
                  # f"accessories: {len(dataset['accessories'])}, {len(dataset['bgames_accessories'])}\n"
                  # f"categories: {len(dataset['categories'])}, {len(dataset['bgames_categories'])}\n"
                  # f"expansions: {len(dataset['expansions'])}, {len(dataset['bgames_expansions'])}\n"
                  # f"families: {len(dataset['families'])}, {len(dataset['bgames_families'])}\n"
                  # f"honors: {len(dataset['honors'])}, {len(dataset['bgames_honors'])}\n"
                  # f"integrations: {len(dataset['integrations'])}, {len(dataset['bgames_integrations'])}\n"
                  # f"mechanics: {len(dataset['mechanics'])}, {len(dataset['bgames_mechanics'])}\n"
                  # f"people: {len(dataset['people'])}, {len(dataset['bgames_people'])}\n"
                  # f"podcasts: {len(dataset['podcasts'])}, {len(dataset['bgames_podcasts'])}\n"
                  # f"publishers: {len(dataset['publishers'])}, {len(dataset['bgames_publishers'])}\n"
                  # f"subdomains: {len(dataset['subdomains'])}, {len(dataset['bgames_subdomains'])}\n"
                  # f"versions: {len(dataset['versions'])}, {len(dataset['bgames_versions'])}\n"
                  # f"bgames: {len(dataset['bgames'])}"
                 )
            if time.time() - time_loop < 3:
                time.sleep(3)
            current_page = page + 1
            print("loop time", time.time() - time_loop)
    except ConnectionError:
        print("got ConnectionError")
        gather_data(current_page, final_page, dataset)


# cleaning all tables in database
def delete_all_data():
    new_session = create_db_session()
    table_list = [dbt.Accessories,
                  dbt.Bgames,
                  dbt.BgamesAccessories,
                  dbt.BgamesCategories,
                  dbt.BgamesExpansions,
                  dbt.BgamesFamilies,
                  dbt.BgamesHonors,
                  dbt.BgamesIntegrations,
                  dbt.BgamesMechanics,
                  dbt.BgamesPeople,
                  dbt.BgamesPodcasts,
                  dbt.BgamesPublishers,
                  dbt.BgamesSubdomains,
                  dbt.BgamesVersions,
                  dbt.Categories,
                  dbt.Expansions,
                  dbt.Families,
                  dbt.Honors,
                  dbt.Integrations,
                  dbt.Mechanics,
                  dbt.People,
                  dbt.Podcasts,
                  dbt.Publishers,
                  dbt.Subdomains,
                  dbt.Versions,
                  ]
    for table in table_list:
        query = new_session.query(table)
        query.delete()
    new_session.commit()
    new_session.close()


# start of work
time_start = datetime.datetime.now()
# creating first page and last page variables
start = 1
finish = get_final_page(creds.BGG_BROWSE_PAGE + "1") + 1
# creating an empty dataset for data from BGG
data = {"bgames": list(),
        "accessories": set(),
        "categories": set(),
        "expansions": set(),
        "families": set(),
        "honors": set(),
        "integrations": set(),
        "mechanics": set(),
        "people": set(),
        "podcasts": set(),
        "publishers": set(),
        "subdomains": set(),
        "versions": set(),
        "bgames_accessories": set(),
        "bgames_categories": set(),
        "bgames_expansions": set(),
        "bgames_families": set(),
        "bgames_honors": set(),
        "bgames_integrations": set(),
        "bgames_mechanics": set(),
        "bgames_people": set(),
        "bgames_podcasts": set(),
        "bgames_publishers": set(),
        "bgames_subdomains": set(),
        "bgames_versions": set(),
        }
# filling up the dataset
gather_data(start, finish, data)
# removing duplicates from bgames if any
data["bgames"] = list({t["objectid"]: t for t in data["bgames"]}.values())
# creating lists with class-based instances for future database filling
accessories, categories, expansions, families, honors, integrations = [], [], [], [], [], []
mechanics, people, podcasts, publishers, subdomains, versions = [], [], [], [], [], []
bgames_accessories, bgames_categories, bgames_expansions, bgames_families = [], [], [], []
bgames_honors, bgames_integrations, bgames_mechanics, bgames_people = [], [], [], []
bgames_podcasts, bgames_publishers, bgames_subdomains, bgames_versions = [], [], [], []
bgames = []
# connections between all entities
data_db_connection_dict = {"accessories": [dbt.Accessories, accessories],
                           "categories": [dbt.Categories, categories],
                           "expansions": [dbt.Expansions, expansions],
                           "families": [dbt.Families, families],
                           "honors": [dbt.Honors, honors],
                           "integrations": [dbt.Integrations, integrations],
                           "mechanics": [dbt.Mechanics, mechanics],
                           "people": [dbt.People, people],
                           "podcasts": [dbt.Podcasts, podcasts],
                           "publishers": [dbt.Publishers, publishers],
                           "subdomains": [dbt.Subdomains, subdomains],
                           "versions": [dbt.Versions, versions],
                           "bgames_accessories": [dbt.BgamesAccessories, bgames_accessories],
                           "bgames_categories": [dbt.BgamesCategories, bgames_categories],
                           "bgames_expansions": [dbt.BgamesExpansions, bgames_expansions],
                           "bgames_families": [dbt.BgamesFamilies, bgames_families],
                           "bgames_honors": [dbt.BgamesHonors, bgames_honors],
                           "bgames_integrations": [dbt.BgamesIntegrations, bgames_integrations],
                           "bgames_mechanics": [dbt.BgamesMechanics, bgames_mechanics],
                           "bgames_people": [dbt.BgamesPeople, bgames_people],
                           "bgames_podcasts": [dbt.BgamesPodcasts, bgames_podcasts],
                           "bgames_publishers": [dbt.BgamesPublishers, bgames_publishers],
                           "bgames_subdomains": [dbt.BgamesSubdomains, bgames_subdomains],
                           "bgames_versions": [dbt.BgamesVersions, bgames_versions],
                           "bgames": [dbt.Bgames, bgames]
                           }

# for next loop:
#     datasource = key in data and connection dict
#     destination[0] = class
#     destination[1] = list for class instances
#     position = row for table in database
for datasource, destination in data_db_connection_dict.items():
    if datasource == "bgames_people":
        for position in data[datasource]:
            destination[1].append(destination[0](position[0], position[1], position[2]))
    elif datasource == "bgames":
        for position in data[datasource]:
            destination[1].append(destination[0](bgame_id=position["objectid"],
                                                 title=position["name"],
                                                 yearpublished=position["yearpublished"],
                                                 min_players=position["minplayers"],
                                                 max_players=position["maxplayers"],
                                                 playtime=position["playingtime"],
                                                 min_playtime=position["minplaytime"],
                                                 max_playtime=position["maxplaytime"],
                                                 age=position["age"],
                                                 thumbnail=position["thumbnail"],
                                                 image=position["image"],
                                                 description=position["description"],
                                                 rank=position["rank"],
                                                 usersrated=position["usersrated"],
                                                 average=position["average"],
                                                 bayesaverage=position["bayesaverage"],
                                                 ))
    else:
        for position in data[datasource]:
            destination[1].append(destination[0](position[0], position[1]))

# clearing the database
print("deleting data from database")
delete_all_data()
print(f"after cleaning the db {datetime.datetime.now() - time_start}")
# writing data to the database
print("time to write data to database")
session = create_db_session()
for destination in data_db_connection_dict.values():
    session.add_all(destination[1])
    session.commit()
print(f"spent {datetime.datetime.now() - time_start}")
