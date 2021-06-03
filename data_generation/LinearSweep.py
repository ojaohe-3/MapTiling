import os
from os import listdir
from os.path import isfile, join
from generateFarmObjects import FarmObject, load_Obj
from poly import get_polyfill
from fetchImages import fetch_single
import numpy as np
from tqdm import tqdm
import shutil
import asyncio

maximum = 750_000

def load_segment(seg) -> [FarmObject]:
    data = []
    print("loading segments:")
    for o in tqdm(seg):
        data.append(load_Obj('./obj/' + o))
    return data

def get_files(start, end):
    data = []
    with open('files.txt', 'r') as f:
        for i in range(start, end):
            f.seek(i*31)
            data.append(f.readline().strip('\n'))
    return data


async def fetch_img(key):
    x,y = key.split('.')
    await fetch_single(x,y, './data/train/FARMLAND')   

async def farm_object_procedure(farm, dic):
    # 1 check if we already have the image move it to folder
    # 2 if not we want to fetch it unless we have done too many fetches
    # 3 generate polygon fill from the object and dump into d file
    # 4 if d file exsist already, load it, then replace it

    for key, item in farm.regions.items():
        if key in dic:
            shutil.move(f'./img/{key}.png', f'./data/train/FARMLAND/{key}.png')
        else:
            await fetch_img(key)
        
        poly_fill = np.array(get_polyfill(item))
        poly_fill = np.clip(poly_fill, 0, 511)

        if (os.path.isfile('./data/train/FARMLAND/')):
            with open(f'./data/train/FARMLAND/{key}.np', 'rb') as f:
                label = np.load(f)
        else:
            label = np.zeros((512,512))

        for x,y in poly_fill:
            label[int(x),int(y)] = 1
        with open(f'./data/train/FARMLAND/{key}.np', 'wb')as f:
            np.save(f,label)

    

async def process_segment(start,end, dic):
    farms = load_segment(get_files(start,end))

    print('processing farm segments')
    for farm in tqdm(farms):
        await farm_object_procedure(farm,dic) 

async def main():
    dic = { key.split('.')[0] : key for key in listdir('./img')}
    segments = list(range(0,1_233_722+12_589, 12_589)) #1233723 items, skip one and divide into 99 parts
    segments = [ [segments[i-1], d] for i,d in enumerate(segments) if i != 0] # split into ranges
    for start, end in segments:
        await process_segment(start,end, dic)

if __name__ == '__main__' :
    asyncio.run(main())

