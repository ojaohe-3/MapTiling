import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models


class FCN(nn.Module):
    """ 
    An attempt on a Fully Convolutional Network
    idea was to identify farmlands by pixel using semantic segmentation, with a binary classifier

    """
    def __init__(self,):
        super().__init__()
        # base net

        net = models.resnet18(pretrained=True)
        net = list(net.children())[:-1]
        self.resnet = nn.Sequential(*net)
        relu = nn.ReLU(inplace=True)

        # fcn net
        self.classifier = nn.Conv2d(32, 1, kernel_size=1) # this is 100% wrong

        self.fcn = nn.Sequential(
            relu,
            nn.ConvTranspose2d(512, 512, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.BatchNorm2d(512),
            relu,
            nn.ConvTranspose2d(512, 256, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.BatchNorm2d(256),
            relu,
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.BatchNorm2d(128),
            relu,
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.BatchNorm2d(64),
            relu,
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),
            nn.BatchNorm2d(32),
            relu
        )


    def forward(self, x):
        # base forward
        x = self.resnet(x)

        # Segmentation
        x = self.fcn(x)
        x = self.classifier(x)

        return x

