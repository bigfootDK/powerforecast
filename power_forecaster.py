from flask import Flask, render_template, Markup
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import geojson

Base = automap_base()

engine = create_engine("sqlite:///powerforecast.db")

# reflect the tables in the database
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Eisman = Base.classes.eisman

app = Flask(__name__)
session = Session(engine)

# id is only used for slide show if not provided it is a static page
def make_plot(timestamp=None, id=None):
    with open('schleswig-holstein.geojson', 'r') as geofile:
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

#ts = [
#'2016-11-10 14:37:46',
#'2016-11-07 08:30:39',
#'2016-11-07 08:30:37',
#'2016-11-07 08:30:36',
#'2016-11-07 08:29:26',
#'2016-11-07 08:29:25',
#'2016-11-07 08:29:22',
#'2016-11-07 08:29:14',
#'2016-11-07 08:29:08',
#'2016-11-07 08:29:05',
#'2016-11-07 07:09:13',
#'2016-11-07 07:08:20',
#'2016-11-07 05:55:22',
#'2016-11-07 05:54:12',
#'2016-11-07 05:51:39',
#'2016-11-07 05:51:28',
#'2016-11-07 05:51:26',
#'2016-11-06 22:30:25',
#'2016-11-06 22:21:07',
#'2016-11-06 22:09:59']


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
