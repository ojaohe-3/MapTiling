
import os
import cv2 
import numpy as np
keys = os.listdir('./data/train/')



i = 0
update = True
while True:
    if update:
        x,y,_ = keys[i].split('.')
        key = f'{x}.{y}'
        with open(f'./data/train/{key}.np', 'rb') as f:
            label = np.load(f)
        label = np.uint8(255 * label)
        label = cv2.applyColorMap(label, cv2.COLORMAP_JET)
        label = label.astype(dtype=np.uint8)
        img = cv2.imread(f'./data/train/{key}.png')

        heatmap = label+img

        img = cv2.resize(img, (512,512))
        heatmap = cv2.resize(heatmap, (512,512))

        cv2.imshow('test1',img) 
        cv2.imshow('test2',label)
        cv2.imshow('test3',heatmap)
        # cv2.waitKey(0)
    update = False

    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(2) == ord(' '):
        i += 2
        update = True

cv2.destroyAllWindows()
