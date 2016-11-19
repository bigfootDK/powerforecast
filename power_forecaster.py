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

def make_plot(timestamp=None):
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
        print(timestamp)
        eismans = session.query(Eisman).filter(Eisman.datetime_ab <= timestamp, Eisman.datetime_bis >= timestamp)
    else:
        eismans = session.query(Eisman).all()
    plot = figure()
    plot.patches(lons, lats, fill_alpha=0.2)
    plot.circle(x=[e.lon for e in eismans],
                y=[e.lat for e in eismans])
    #html = file_html(plot, CDN, "my plot")
    script, div = components(plot)
    return render_template('ui.html', script=Markup(script), div=Markup(div))

@app.route('/')
def index():
    return make_plot()


@app.route('/<timestamp>')
def timestamp(timestamp):
    return make_plot(timestamp)


if __name__ == '__main__':
    app.run(debug=True)
