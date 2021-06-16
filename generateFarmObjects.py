import json
from poly import xtile, ytile, getPixel, get_polyfill
from concurrent.futures import ProcessPoolExecutor, as_completed
import pickle
from time import sleep, time
import numpy as np
from tqdm import tqdm

def worker(data):
    # print('got a fragment of data', len(data), "units long")
    objs = []
    for e in (data):
        obj = FarmObject(e)
        _id = e["_id"]["$oid"]
        objs.append(obj)
        # print('added object!')
    with open(f'./obj/{_id}.dump', 'wb') as f:
        pickle.dump(objs,f)
        # print(f'{_id} added')

class FarmObject:
    """
    Serializeable data, contation all region polygons that encapsulate a single farm.
    """
    def __init__(self, raw_data):
        super().__init__()
        self.regions = {}
        data =  raw_data['geometry']['coordinates']
        for p in data:
            if len(p[0]) <= 2:
                for lon,lat in p:
                    x = xtile(lon)
                    y = ytile(lat)
                    pix = getPixel(lon,lat,256)
                    key = f'{x}.{y}'

                    if(key in self.regions):
                        if self.regions[key].shape == (2,):
                            self.regions[key] = np.stack((self.regions[key], pix))
                        else:
                            self.regions[key] = np.concatenate((self.regions[key], [pix]))
                    else:
                        self.regions[key] = pix
            # if the json parses bad data, and adds a extra 0 value
            elif len(p[0]) == 3:
                for lon,lat,_ in p:
                    x = xtile(lon)
                    y = ytile(lat)
                    pix = getPixel(lon,lat,256)
                    key = f'{x}.{y}'

                    if(key in self.regions):
                        if self.regions[key].shape == (2,):
                            self.regions[key] = np.stack((self.regions[key], pix))
                        else:
                            self.regions[key] = np.concatenate((self.regions[key], [pix]))
                    else:
                        self.regions[key] = pix

            if len(self.regions) > 1:
                self.intersect_region()

    def intersect_region(self):
        pos0, points = next(iter(self.regions.items()))
        x0, y0 = pos0.split('.')
        x0 = int(x0)
        y0 = int(y0)

        intr_r1 = []
        intr_r2  = []
        for pos, ps in self.regions.items():
            if pos != pos0 and ps.shape != (2,):
                x, y = pos.split('.')
                x = int(x)
                y = int(y)
                dx = x - x0
                dy = y - y0
                
                r1, r2 = self.bound_intersection(points, ps, dx, dy, (256, 256))
                intr_r1.append(r1)
                intr_r2.append(r2)
                
                for p in intr_r2:
                    self.regions[pos] = np.concatenate((self.regions[pos], p))
        for p in intr_r1:
            self.regions[pos0] = np.concatenate((self.regions[pos0], p))



    def bound_intersection(self, box1, box2, dx, dy,bounds):
        """ Finds regions bounds intersection, assuming it is convex

        Args:
            box1 ([[int]]):  polygon that clip into region 1 based on its pixel values for that specific region
            box2 ([[int]]): polygon that clip into region 2 based on its pixel values for that specific region
            dx (int): the relative x between region1 and 2 based on is tile number
            dy (int): the relative y between region1 and 2 based on is tile number
            bounds ((int, int)): the bounding box of the region based on its pixel value

        Returns:
            [[r1][r2]]: intersection points to region 1 (r1), and region 2 (r2)
        """
        w, h = bounds

        
        if dx == 0:
            max_x = np.max(box1[:,0])
            min_x = np.min(box1[:,0])

            max_x1 = np.max(box2[:,0])
            min_x1 = np.min(box2[:,0])

            if dy > 0:
                return np.array([[min_x, h], [max_x, h]]), np.array([[min_x1, 0], [max_x1, 0]])
            else:
                return np.array([[min_x, 0], [max_x, 0]]), np.array([[min_x1, h],[max_x1, h]])
        elif dy == 0:
            max_y = np.max(box1[:,1])
            min_y = np.min(box1[:,1])

            max_y1 = np.max(box2[:,1])
            min_y1 = np.min(box2[:,1])

            if dx > 0:
                return np.array([[w, min_y], [w, max_y]]), np.array([[0, min_y1], [0, max_y1]])
            else:
                return np.array([[0, min_y], [0, max_y]]), np.array([[w, min_y1],[w, max_y1]])
        else:
            if dx > 0:
                r1_x = w
                r2_x = 0
            else:
                r1_x = 0
                r2_x = w
            if dy > 0:
                r1_y = h
                r2_y = 0
            else:
                r1_y = 0
                r2_y = h
            return np.array([[r1_x,r1_y]]), np.array([[r2_x, r2_y]])

        


def main():
    print('loading large json')
    t = time()
    with open('trainingDataFields.json') as f:
        data = json.load(f)

    print('finished loading after',time()-t,'s')
    n = int(len(data)/100)

    regions = [data[i:i + n] for i in range(0, len(data), n)]

    # worker(regions[0])
    with ProcessPoolExecutor(max_workers = 8) as pool:
        
        futures = [pool.submit(worker, region) for region in regions]
        kwargs = {
        'total': len(futures),
        'unit': 'it',
        'unit_scale': True,
        'leave': True
        }

        #Print out the progress as tasks complete
        for f in tqdm(as_completed(futures), **kwargs):
            pass

def load_Obj(fn):
    with open(fn, 'rb') as f:
        data = pickle.load(f)
    return data
if __name__ == '__main__' :
    main()