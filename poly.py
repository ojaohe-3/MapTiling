import json
import numpy as np
import mahotas
z = 15
n = np.power(2, z)

def generate_polygon():
    """
    Generates polygons of sweden.
    Generates a polygon of each iland.
    e.g. gotland and mainland

    """
    with open('sweden.json') as f:
        data = json.load(f)

        arr = data['geometry']['coordinates']
        dt = []
        res = []
        for x in arr:
            for poly in x:
                for p in poly:
                    dt.append(p)
                res.append(dt)
                dt = []
    


    for i,p in enumerate(res):
        res[i] = np.array([[ xtile(x), ytile(y)] for x,y in p])

    return res


def xtile(lon):
    return int(n * ((lon+180)/360))


def ytile(lat):
    rad = np.deg2rad(lat)
    return int(n * (1-np.log(np.tan(rad) + (1/np.cos(rad)))/np.pi)/2)

def getPixel(lon, lat, size):
    rad = np.deg2rad(lat)
    res = np.array([ (n * ((lon+180)/360) - xtile(lon)),  (n * (1-np.log(np.tan(rad) + (1/np.cos(rad)))/np.pi)/2 - ytile(lat))])
    return np.round(res * size)


def get_polyfill(poly):
    """Return polygon as grid of points inside polygon.

    Input : poly (list of lists)
    Output : output (list of lists)
    """
    xs, ys = zip(*poly)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    newPoly = [(int(x - minx), int(y - miny)) for (x, y) in poly]

    X = maxx - minx + 1
    Y = maxy - miny + 1

    grid = np.zeros((X, Y), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)

    return [(x + minx, y + miny) for (x, y) in zip(*np.nonzero(grid))]





# import matplotlib.pyplot as plt

# data = generate_polygon()
# get_polyfill(data[0])
# plt.figure(None, (5, 5))
# x, y = zip(*get_polyfill(example))
# plt.scatter(x, y)
# x, y = zip(*example)
# plt.plot(x, y, c="r")
# plt.show()