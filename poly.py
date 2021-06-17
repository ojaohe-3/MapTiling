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
    x = xtile(lon)
    y = ytile(lat)

    x0,y0 = num2deg(x,y)
    x1,y1 = num2deg(x+1,y+1)

    ux = np.array([x1-x0,0])
    uy = np.array([0,y1-y0])
    

    res = np.array([(1/(np.linalg.norm(ux)))*(lon - x0), (1/(np.linalg.norm(uy)))*(lat - y1)])


    # find the unit vector of lon/lan then project up to img size, this is naive, because lon, lat is not euclidian
    return np.round(res*size)
    
   
def num2deg(x, y):
  lon_deg = x / n * 360.0 - 180.0
  lat_rad = np.arctan(np.sinh(np.pi * (1 - 2 * y / n)))
  lat_deg = np.rad2deg(lat_rad)
  return (lon_deg, lat_deg)

   


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

    grid = np.zeros((int(X), int(Y)), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)

    return [(x + minx, y + miny) for (x, y) in zip(*np.nonzero(grid))]



if __name__ == '__main__' :
    import matplotlib.pyplot as plt

    data = generate_polygon()
    x, y = zip(*get_polyfill(data[-1]))
    plt.scatter(x, y)
    # plt.plot(x, y, c="r")
    plt.show()