from flask import Flask, render_template, request
import functions as fn
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", param_1={}, game_list={})


@app.route("/show")
def show_games():
    num_games = int(request.args.get("num_games"))
    sort = request.args.get("sort")
    sort_dir = request.args.get("sort_dir")
    games_dict = fn.get_dict_with_all_games(num_games, sort, sort_dir)

    index_for_th = random.choice(list(games_dict.keys()))
    game_list_for_th = games_dict[index_for_th].keys()

    return render_template("index.html",
                           param_1=list(games_dict.values()),
                           game_list_for_th=game_list_for_th,
                           game_list=games_dict)

