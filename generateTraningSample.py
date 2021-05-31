import json
from poly import xtile, ytile, getPixel, get_polyfill
from concurrent.futures import ProcessPoolExecutor
import pickle
import time


def worker(data):
    print('got a fragment of data', len(data), "units long")
    for i,e in enumerate(data):
        obj = FarmObject(e)
        print("e:",e, "\nobj:",obj)
        print('object created, dumping into', f'{i}.dump')
        with open(f'./obj/{i}.dump', 'w') as f:
            pickle.dump(obj,f)
            print(f'{i} added')

class FarmObject:
    def __init__(self, raw_data):
        super().__init__()
        self.regions = {}
        for lon,lat in raw_data['geometry']['coordinates']:
            print(lon,lat)
            x = xtile(lon)
            y = ytile(lat)
            p = getPixel(lon,lat,512)
            key = f'{x}.{y}'

            if(key in self.regions):
                self.regions[key].append(p)
            else:
                self.regions[key] = [p]
    
def main():
    print('loading large traningset')
    t = time.time()
    with open('trainingDataFields.json') as f:
        data = json.load(f)
    print('finished loading after',time.time()-t,'s')
    n = int(len(data)/24)
    regions = [data[i:i + n] for i in range(0, len(data), n)]
    worker(regions[0])
    # with ProcessPoolExecutor(max_workers = 5) as executor:
    #     for region in regions:
    #         executor.submit(worker, region)

if __name__ == '__main__' :
    main()