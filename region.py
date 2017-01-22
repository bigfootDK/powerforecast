import geojson


class Region:
    __x = list()
    __y = list()

    def __init__(self, geojson_filename):
        with open('data/{}'.format(geojson_filename), 'r') as geofile:
            region = geojson.load(geofile)
            features = region['features']

        for feature in features:
            if feature['geometry']['type'] == 'Polygon':
                coords = [feature['geometry']['coordinates']]
            else:
                coords = feature['geometry']['coordinates']

            for coord in coords:
                self.__x.append([c[0] for c in coord[0]])
                self.__y.append([c[1] for c in coord[0]])

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
