from flask import Flask, render_template

import configuration
from dimmer_client import request_set_light_levels


app = Flask(__name__)

columns = int(12 / len(configuration.rooms))


@app.route("/")
def main_page():
    return render_template('main.html', rooms=configuration.rooms, columns=columns,
                           levels=configuration.levels_tuple, current_level=-1)


@app.route("/<room>/set_level/<level>")
def user_profile(room, level):
    request_set_light_levels({room: int(level)})
    return render_template('main.html', rooms=configuration.rooms, columns=columns,
                           levels=configuration.levels_tuple, current_level=int(level))

# $ set FLASK_APP=dimmer_site.py
# $ flask run
