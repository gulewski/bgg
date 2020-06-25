from flask import Flask, render_template, request
import functions as fn
import random
import json

app = Flask(__name__)


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

    if games_dict:
        index_for_th = random.choice(list(games_dict.keys()))
        game_list_for_th = games_dict[index_for_th].keys()
        all_games = list(games_dict.values())
    else:
        game_list_for_th = {}
        all_games = []

    return render_template("search.html",
                           search_string=search_string,
                           exact=exact,
                           game_list=games_dict,
                           show_first=5,
                           all_games=all_games,
                           game_list_for_th=game_list_for_th,
                           )
