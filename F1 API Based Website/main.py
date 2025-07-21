from flask import Flask, abort, render_template, redirect, url_for, flash, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your Secret Key'


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/drivers")
def drivers():
    url = "https://f1api.dev/api/current/drivers"
    response = requests.get(url)
    data = response.json()
    drivers = data["drivers"]
    return render_template("drivers.html", drivers=drivers)


@app.route("/teams")
def teams():
    url = "https://f1api.dev/api/current/teams"
    response = requests.get(url)
    data = response.json()
    teams = data["teams"]
    return render_template("teams.html", teams=teams)

@app.route("/results")
def results():
    races = []
    result = []
    for number in range(1, 13):
        url = f"https://f1api.dev/api/2025/{number}/race"
        response = requests.get(url)
        data = response.json()
        races.append(data["races"])
        result.append(data["races"]["results"][0]["driver"])
    return render_template("result.html", races=races, results=result)

@app.route("/champion-ship")
def champion_ship():
    url = "https://f1api.dev/api/current/drivers-championship"
    response = requests.get(url)
    data = response.json()
    current = data["drivers_championship"]
    return render_template("champship.html", current_standing=current)

@app.route("/upcoming-races")
def races():
    url = "https://f1api.dev/api/current/next"
    response = requests.get(url)
    data = response.json()
    races = data["race"]
    date = data["race"][0]["schedule"]["race"]
    return render_template("next_races.html", next_races=races, date=date)

@app.route("/circuits")
def circuits():
    url = "https://f1api.dev/api/circuits"
    response = requests.get(url)
    data = response.json()
    tracks = data["circuits"]
    return render_template("circuits.html", tracks=tracks)
if __name__ == "__main__":
    app.run(debug=True, port=5002)
