from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from utilities import parse_time, date2delta


class Eisman:
    __day_max = int()
    __day_min = int()

    __x = list()
    __y = list()
    
    __level = list()  # regelstufe
    __energy_source = list()

    def __init__(self, database_name):
        engine = create_engine("sqlite:///data/{}".format(database_name))
        base = automap_base()
        base.prepare(engine, reflect=True)

        self.__eisman = base.classes.eisman
        self.__session = Session(engine)
       
    def set_data(self, days_limit): 
        eis = self.__session.query(self.__eisman).all()

        # lists of empy lists (nested)
        self.__x = [[list() for __ in range(25)] for _ in range(days_limit)]
        self.__y = [[list() for __ in range(25)] for _ in range(days_limit)]
        self.__level = [[list() for __ in range(25)] for _ in range(days_limit)]
        self.__energy_source = [[list() for __ in range(25)] for _ in range(days_limit)]

        self.__day_max = 0
        self.__day_min = days_limit

        for e in eis:
            day_start = date2delta(parse_time(e.datetime_ab))
            extra_days = date2delta(parse_time(e.datetime_bis)) - day_start

            hour_start = int(e.datetime_ab[11:13])
            hour_stop = int(e.datetime_bis[11:13])

            for xtra_day in range(extra_days+1):
                running_day = day_start + xtra_day

                if running_day < days_limit:
                    # adapt timestap range
                    if self.__day_max < running_day:
                        self.__day_max = running_day
                    if self.__day_min > running_day:
                        self.__day_min = running_day

                    self.set_data_for_hour(running_day, 24, e)

                    if xtra_day == 0:
                        hour_start_of_running_day = hour_start
                    else:
                        hour_start_of_running_day = 0
                    
                    if xtra_day == extra_days:
                        hour_stop_of_running_day = hour_stop
                    else:
                        hour_stop_of_running_day = 24

                    for running_hour in range(hour_start_of_running_day, hour_stop_of_running_day):
                        self.set_data_for_hour(running_day, running_hour, e)

    def set_data_for_hour(self, day, hour, eisman_case):
        self.__x[day][hour].append(eisman_case.lon)
        self.__y[day][hour].append(eisman_case.lat)

        append_to_eisman_variable(self.__level[day][hour],
                                  eisman_case.regelstufe_einspeisermanagement,  # circle size
                                  {'000': '10',  # complete shutdown
                                   '030': '6', '031': '6',
                                   '060': '3'})
        append_to_eisman_variable(self.__energy_source[day][hour],
                                  eisman_case.energy_source_level_2,  # circle color
                                  {'Wind': 'blue',
                                   'Bioenergy': 'green'})
               
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def day_min(self):
        return self.__day_min

    @property
    def day_max(self):
        return self.__day_max

    @property
    def level(self):
        return self.__level

    @property
    def energy_source(self):
        return self.__energy_source


def append_to_eisman_variable(eisman_variable, database_entry, options_dict):
    eisman_variable.append(options_dict[database_entry])
