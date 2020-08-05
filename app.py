from flask import Flask, render_template, request
import functions as fn
import random

app = Flask(__name__)

aliases = {'rank': 'Game rank',
           'title': 'Title',
           # 'alt_titles': 'Alternative titles',
           'thumbnail': 'Box image',
           # 'image': 'Image',
           'usersrated': 'Num voters',
           'average': 'Avg rating',
           'bayesaverage': 'BGG rating',
           'yearpublished': 'Year',
           'minplayers': 'MIN players',
           'maxplayers': 'MAX players',
           'minplaytime': 'MIN playtime',
           'maxplaytime': 'MAX playtime',
           'age': 'Age',
           # 'description': 'Description',

           'boardgamedesigner': 'Designers',
           'boardgameartist': 'Artists',
           'boardgamepublisher': 'Publishers',
           'boardgamecategory': 'Categories',
           'boardgamemechanic': 'Mechanics',
           'boardgamefamily': 'Family',
           'boardgamesubdomain': 'Subdomain',
           'boardgameexpansion': 'Expansions',
           'boardgameintegration': 'Integrations',
           'boardgame': 'Integrations',

           'boardgamepodcastepisode': 'Podcasts',
           'boardgamehonor': 'Honors',
           'boardgameversion': 'Versions',
           # 'videogamebg': 'Videogame',
           'boardgameaccessory': 'Accessories',
           }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show")
def show_games():
    num_games = int(request.args.get("num_games"))
    sort = request.args.get("sort")
    sort_dir = request.args.get("sort_dir")
    games_dict = fn.get_games_info(quantity_games=num_games, sort_by=sort, sort_dir=sort_dir)

    index_for_th = random.choice(list(games_dict.keys()))
    game_list_for_th = games_dict[index_for_th].keys()

    # print(json.dumps(games_dict, indent=2, ensure_ascii=False))

    return render_template("show.html",
                           aliases=aliases,
                           all_games=list(games_dict.values()),
                           game_list_for_th=game_list_for_th,
                           game_list=games_dict,
                           show_first=5,
                           num_games=num_games,
                           sort=sort,
                           sort_dir=sort_dir)


@app.route("/search")
def search():
    search_string = request.args.get("search_string")
    exact = request.args.get("exact")
    if exact is None:
        exact = 0
    else:
        exact = 1
    games_dict = fn.get_games_info(search_string=search_string, exact=exact)

    game_list_for_th = {}
    all_games = []

    if games_dict:
        index_for_th = random.choice(list(games_dict.keys()))
        game_list_for_th = games_dict[index_for_th].keys()
        all_games = list(games_dict.values())

    return render_template("search.html",
                           aliases=aliases,
                           search_string=search_string,
                           exact=exact,
                           game_list=games_dict,
                           show_first=5,
                           all_games=all_games,
                           game_list_for_th=game_list_for_th,
                           )


if __name__ == '__main__':
    app.run()
