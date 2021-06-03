import os
import numpy as np

files = os.listdir('./data/train')
dic = {}
for f in files:
    x,y, _ = f.split('.')
    key = x+'.'+y
    if key in dic: 
        dic[key].append(f)
    else:
        dic[key] = [f]


from tqdm import tqdm
p = np.random.normal(size=len(dic))
for i, pair in tqdm(enumerate(dic.values())):

    # 5 % probability
    if p[i] < -1.66:
        prefix = './data/test/'
        # 0.1% probability
        if p[i] < -3.1:
            prefix = './data/val/'

        for item in pair:
            os.replace('./data/train/'+item, prefix+item)        

