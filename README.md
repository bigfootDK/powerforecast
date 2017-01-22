# powerforecast

The power forecaster for idealists (in development).

Shall predicts the contributions of solar and wind energy in the power network
of Schleswig-Holstein for the following 24 hours. This tells us Fischkoepfe if
we should do our laundry right now or better wait for a few hours.

Initiated at [KreativHack 2016 in Kiel](https://wiki.kreativhack.de/kh16/projects/powerforecast/start).


## How to install and run it

You can test this development version. Just download or clone this repository.
The scripts are made for python 3.4 and python 3.5 so far. Install the
requirements with pip:

```bash
pip install -r requirements.txt
```

And run:

```bash
python webapp.py
```

Then point your webbrowser to
[http://localhost:5000](http://localhost:5000) to see the actual state.


## Need help?

Just open an [issue](https://github.com/bigfootDK/powerforecast/issues).


## Data used

* [Renewabale power plants in Germany by OSPD](http://data.open-power-system-data.org/renewable_power_plants/)

* [Einspeisemanagement-Einsätze by Schleswig-Holstein Netz AG](https://www.sh-netz.com/cps/rde/xchg/sh-netz/hs.xsl/2472.htm)

