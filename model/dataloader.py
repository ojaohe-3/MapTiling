import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import numpy as np
import os
import cv2
class MapTiles(torch.utils.data.Dataset):
    """Some Information about MapTiles"""
    def __init__(self, path, transform=None):
        super(MapTiles, self).__init__()
        self.path = path
        self.list_path = os.listdir(path)
        self.transform = transform

    def __getitem__(self, index):
        x,y,_ = self.list_path[index*2].split('.')
        with open(f"{x}{y}.np", "rb") as f:
            label = np.load(f)
        image = cv2.imread(self.path)
        
        if self.transform:
            image = self.transform(image)
            label = self.transform(label)
            
        return image, label

    def __len__(self):
        return len(self.list_path)/2