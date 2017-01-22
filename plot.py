from bokeh.plotting import figure
from bokeh.embed import components


class Plot:
    def __init__(self):
        self.__plot = figure(tools='save', plot_width=400, plot_height=400)
        self.__plot.toolbar.logo = None
        self.__plot.xaxis.visible = False
        self.__plot.yaxis.visible = False

    def set_region(self, region):
        self.__plot.patches(region.x, region.y, color="olive", alpha=0.2)

    def set_eisman_data(self, eisman, day, hour):
        self.__plot.circle(x=eisman.x[day][hour], y=eisman.y[day][hour], color=eisman.energy_source[day][hour],
                           size=eisman.level[day][hour], alpha=0.2)

    def create_plot(self):
        return components(self.__plot)
