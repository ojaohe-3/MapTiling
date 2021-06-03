import json
from poly import xtile, ytile, getPixel, get_polyfill
from concurrent.futures import ProcessPoolExecutor
import pickle
from time import sleep, time

def worker(data):
    print('got a fragment of data', len(data), "units long")

    for e in (data):
        obj = FarmObject(e)
        _id = e["_id"]["$oid"]
        with open(f'./obj/{_id}.dump', 'wb') as f:
            pickle.dump(obj,f)
            # print(f'{_id} added')

class FarmObject:
    def __init__(self, raw_data):
        super().__init__()
        self.regions = {}
        data =  raw_data['geometry']['coordinates']
        for p in data:
            if len(p[0]) <= 2:
                for lon,lat in p:
                    x = xtile(lon)
                    y = ytile(lat)
                    pix = getPixel(lon,lat,512)
                    key = f'{x}.{y}'

                    if(key in self.regions):
                        self.regions[key].append(pix)
                    else:
                        self.regions[key] = [pix]
            elif len(p[0]) == 3:
                for lon,lat,_ in p:
                    x = xtile(lon)
                    y = ytile(lat)
                    pix = getPixel(lon,lat,512)
                    key = f'{x}.{y}'

                    if(key in self.regions):
                        self.regions[key].append(pix)
                    else:
                        self.regions[key] = [pix]
def main():
    print('loading large traningset')
    t = time()
    with open('trainingDataFields.json') as f:
        data = json.load(f)
    print('finished loading after',time()-t,'s')
    n = int(len(data)/10)
    regions = [data[i:i + n] for i in range(0, len(data), n)]
    with ProcessPoolExecutor(max_workers = 10) as executor:
        for region in regions:
            executor.submit(worker, region)

def load_Obj(fn):
    with open(fn, 'rb') as f:
        data = pickle.load(f)
    return data
if __name__ == '__main__' :
    main()