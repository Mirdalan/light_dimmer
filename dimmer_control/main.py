from flask import Flask, url_for, render_template, redirect

import configuration
from dimmer_client import request_set_light_levels


app = Flask(__name__)

columns = int(12 / len(configuration.rooms))


@app.route("/")
def main_page():
    return render_template('main.html', rooms=configuration.rooms, columns=columns, levels=tuple(range(0, 101, 10)))


@app.route("/<room>/set_level/<level>")
def user_profile(room, level):
    request_set_light_levels({room: int(level)})
    return redirect('/')

# $ set FLASK_APP=main.py
# $ flask run
