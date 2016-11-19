from flask import Flask
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
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


@app.route('/')
def index():
    with open('schleswig-holstein.geojson', 'r') as geofile:
        sh = geojson.load(geofile)
    features = sh['features']
    lons = []
    lats = []
    for feature in features:
        coords = list(geojson.utils.coords(feature))
        lons.append([c[0] for c in coords])
        lats.append([c[1] for c in coords])
    eismans = session.query(Eisman).all()
    plot = figure()
    plot.patches(lons, lats, fill_alpha=0.2)
    plot.circle(x=[e.lon for e in eismans],
                y=[e.lat for e in eismans])
    html = file_html(plot, CDN, "my plot")
    return html


if __name__ == '__main__':
    app.run(debug=True)
