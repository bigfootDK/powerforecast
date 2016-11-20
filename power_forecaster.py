"""This is the main file for powerforecast.

Usage:
Run python power_forecaster.py and point your webbrowser to
<http://localhost:5000>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from flask import Flask, render_template, Markup
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import geojson

Base = automap_base()

engine = create_engine("sqlite:///data/powerforecast.db")

# reflect the tables in the database
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Eisman = Base.classes.eisman

app = Flask(__name__)
session = Session(engine)


# id is only used for slide show if not provided it is a static page
def make_plot(timestamp=None, id=None):
    with open('data/schleswig-holstein.geojson', 'r') as geofile:
        sh = geojson.load(geofile)
    features = sh['features']
    lons = []
    lats = []
    for feature in features:
        if feature['geometry']['type'] == 'Polygon':
            coords = [feature['geometry']['coordinates']]
        else:
            coords = feature['geometry']['coordinates']
        for coord in coords:
            lons.append([c[0] for c in coord[0]])
            lats.append([c[1] for c in coord[0]])
    if timestamp:
        eismans = session.query(Eisman).filter(Eisman.datetime_ab <= timestamp,
                                               Eisman.datetime_bis >= timestamp)
    else:
        eismans = session.query(Eisman).all()
    plot = figure()
    plot.patches(lons, lats, fill_alpha=0.2)
    plot.circle(x=[e.lon for e in eismans],
                y=[e.lat for e in eismans],
                size=10)
    script, div = components(plot)
    return render_template('ui_show.html', script=Markup(script),
                            div=Markup(div), id=id, timestamp=timestamp)


connection = engine.connect()
sql = "SELECT datetime_bis FROM eisman GROUP BY datetime_bis ORDER BY datetime_bis DESC LIMIT 0,200;"
result =  connection.execute(sql)

ts = []
for row in result:
    ts.append(row[0][:-7])
connection.close()


@app.route('/')
@app.route('/<int:id>')
def timestamp(id=0):
    return make_plot(timestamp=ts[id], id=None)


@app.route('/show/<int:id>')
def start_show(id):
    if id == 199:
        return make_plot(timestamp=ts[id], id=None)
    return make_plot(timestamp=ts[id], id=id)


if __name__ == '__main__':
    app.run(debug=True)
