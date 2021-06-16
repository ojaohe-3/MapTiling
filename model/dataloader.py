import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import numpy as np
class MapTiles(torch.utils.data.Dataset):
    """Some Information about MapTiles"""
    def __init__(self, path):
        super(MapTiles, self).__init__()
        
    def __getitem__(self, index):
        return 

    def __len__(self):
        return 