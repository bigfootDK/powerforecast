from flask import Flask, render_template, Markup, request
from plot import Plot
from eisman import Eisman
from region import Region
from utilities import delta2date

eis = Eisman("powerforecast.db")
eisman_max_number_of_days = 5000
eis.set_data(eisman_max_number_of_days)
regio = Region("schleswig-holstein.geojson")

app = Flask(__name__)

day= int(eis.day_min)
time_marching = False  # flag for 'Einsatzverlauf'


def show_plot(day, hour):
    global time_marching

    plot = Plot()
    plot.set_region(regio)
    plot.set_eisman_data(eis, day, hour)
    script, div = plot.create_plot()

    return render_template('eisman.html', script=Markup(script), div=Markup(div), date=delta2date(day),
                           day=day, day_max=eis.day_max, day_min=eis.day_min,
                           hour=hour, time_marching=time_marching)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', day_min=eis.day_min, time_marching=False)


@app.route('/eisman/<int:day>/<int:hour>', methods=['GET', 'POST'])
def eisman(day, hour):
    global time_marching

    if request.form.getlist('day'):
        day = int(request.form['day'])
    if request.form.getlist('hour'):
        hour = int(request.form['hour'])
    if request.form.getlist('time_marching') == ['Zeige Einsatzverlauf']:
        time_marching = True
    if request.form.getlist('time_marching') == ['Anhalten']:
        time_marching = False

    return show_plot(day, hour)


@app.route('/prediction')
def prediction():
    return render_template('prediction.html', day_min=eis.day_min, time_marching=False)


@app.route('/data')
def data():
    return render_template('data.html', day_min=eis.day_min, time_marching=False)


@app.route('/impressum')
def impressum():
    return render_template('impressum.html', day_min=eis.day_min, time_marching=False)


@app.route('/contact')
def contact():
    return render_template('contact.html', day_min=eis.day_min, time_marching=False)


if __name__ == '__main__':
    app.run(debug=True)
