from flask import Flask, render_template
from datetime import date
import cfbd
import os

API_KEY = os.environ.get("API_KEY")
API_KEY_PREFIX = os.environ.get("API_KEY_PREFIX")

app = Flask(__name__)

configuration = cfbd.Configuration()
configuration.api_key["Authorization"] = API_KEY
configuration.api_key_prefix["Authorization"] = API_KEY_PREFIX

teams_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
ranks_instance = cfbd.RankingsApi(cfbd.ApiClient(configuration))

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/byu/roster")
def byu_roster():
	team = "byu"
	roster = teams_instance.get_roster(team=team, year=date.today().year)

	return render_template("roster.html", roster=roster)

@app.route("/byu/games")
def byu_games():
	team = "byu"
	games = games_instance.get_games(year=date.today().year, team=team)
	
	return render_template("games.html", games=games)

@app.route("/uofu/roster")
def uofu_roster():
	team = "Utah"
	roster = teams_instance.get_roster(team=team, year=date.today().year)

	return render_template("roster.html", roster=roster)

@app.route("/uofu/games")
def uofu_games():
	team = "Utah"
	games = games_instance.get_games(year=date.today().year, team=team)
	
	return render_template("games.html", games=games)
	
@app.route("/utah-state/roster")
def utah_state_roster():
	team = "Utah State"
	roster = teams_instance.get_roster(team=team, year=date.today().year)[:-1]
	
	return render_template("roster.html", roster=roster)

@app.route("/utah-state/games")
def utah_state_games():
	team = "Utah State"
	games = games_instance.get_games(year=date.today().year, team=team)
	
	return render_template("games.html", games=games)

@app.route("/rankings")
def rankings():
	rankings = ranks_instance.get_rankings(year=date.today().year)
	
	rankings = rankings[-1].to_dict()["polls"]
	for i in range(len(rankings)):
		if rankings[i]["poll"] == "AP Top 25":
			rankings = rankings[i]["ranks"]
			break
	return render_template("rankings.html", rankings=rankings)

def main():
	app.run()

if __name__ == "__main__":
	main()