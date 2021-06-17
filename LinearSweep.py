from threading import Thread
from concurrent.futures.process import ProcessPoolExecutor
from time import sleep
import os
from os import listdir
from os.path import isfile, join
from generateFarmObjects import FarmObject, load_Obj
from poly import get_polyfill
from fetchImages import run_multi_fetch
import numpy as np
from tqdm import tqdm
import shutil
import cv2


flist = os.listdir('./obj')


def load_segment(seg) -> [FarmObject]: 
    print("loading segments:")
    data = []
    for o in tqdm(seg):
        data.append(load_Obj('./obj/' + o))
    print(f"segment loaded {len(data[0])} farms ")
    return data

def farm_object_procedure(farms): 
    farms = [farm for obj in farms for farm in obj] # flatten
    n = int(len(farms)/120)
    regions = [farms[i:i + n] for i in range(0, len(farms), n)]
    with ProcessPoolExecutor(max_workers=8) as executor:
        for region in regions:
            executor.submit(work, region)

def work(region):
    for farm in region:
        for key, item in farm.regions.items():
            poly_fill = np.array(get_polyfill(item))
            poly_fill = np.clip(poly_fill, 0, 255)
            intr_label = np.zeros((256, 256))
            if (os.path.isfile(f'./data/train/{key}.np')):
                with open(f'./data/train/{key}.np', 'rb') as f:
                    label = np.load(f)
            else:
                label = np.zeros((256, 256))

            for x, y in poly_fill:
                intr_label[int(x), int(y)] = 1
            intr_label = cv2.rotate(intr_label, cv2.ROTATE_90_COUNTERCLOCKWISE)
            label = label + intr_label
            label = label.clip(0,1)
            with open(f'./data/train/{key}.np', 'wb')as f:
                np.save(f, label)

def sweeper(region):
    nr = 0
    C = {}
    for farm in region: 
        for key, item in farm.regions.items():
            if farm.regions[key].shape != (2,): #ignore single point regions
                if key in C:
                    poly_fill = np.array(get_polyfill(item))
                    poly_fill = np.clip(poly_fill, 0, 255)
                    C[key].append(poly_fill)
                    nr += 1
                elif (os.path.isfile(f'./data/train/{key}.np')):
                    poly_fill = np.array(get_polyfill(item))
                    poly_fill = np.clip(poly_fill, 0, 255)
                    C[key] = [poly_fill]
                    nr += 1
    print(f'complimentary step, unloading {nr} to files')
    for key , poly_fills in C.items():
        intr_label = np.zeros((256,256))      
        with open(f'./data/train/{key}.np', 'rb') as f:
            label = np.load(f)
        for poly_fill in poly_fills:
            for x, y in poly_fill:
                intr_label[int(x), int(y)] = 1

        intr_label = cv2.rotate(intr_label, cv2.ROTATE_90_COUNTERCLOCKWISE)
        label = label + intr_label
        label = label.clip(0,1)
        with open(f'./data/train/{key}.np', 'wb')as f:
            np.save(f, label)
    print(f'segment completed, {nr} segments modified!')


def sweep_procedure(farms):
    farms = [farm for obj in farms for farm in obj] # flatten
    n = int(len(farms)/120)
    regions = [farms[i:i + n] for i in range(0, len(farms), n)]
    for region in regions:
        sweeper(region)
    # with ProcessPoolExecutor(max_workers=8) as executor:
    #     executor.map(sweeper, regions)



def process_segment(start, end):
    farms = load_segment(flist[start:end])
    print('processing farm segments')
   
    sweep_procedure(farms)

    # fetch_imgs(fetch_list)


def generate_data(start, end):
    print('generating first farm segment files')
    farms = load_segment(flist[start:end])
    farm_object_procedure(farms)


def main():
    segments = list(range(0, len(flist), 10))
    segments = [[segments[i-1], d]
                for i, d in enumerate(segments) if i != 0]  # split into ranges
    s, e  = segments[0]
    generate_data(s,e)

    for start, end in segments[:1]:
        process_segment(start,end)
        # breaks


if __name__ == '__main__':
    main()
