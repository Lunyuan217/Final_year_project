# -*- coding: utf-8 -*-
"""Main_plot_alpha.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IX0DceM_PSGZCByr33hMcpSViBbWJ6sX
"""

import scipy.io as io
import os
import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms
import torch.nn as nn
from torch.autograd import Variable
import matplotlib.pyplot as plt
from torch_radon import Radon, RadonFanbeam
from kornia import rotate
from random import choice
from network_arch import UNet
from data import dataloader_train,dataloader_test
from utils import PSNR_cal,show_images
from train import EI_train,Supervised_train
from test import EI_test,Supervised_test

epochs=5000
batch_size=2
learning_rate=0.0005
weight_dec=1e-8
image_size=128
det_count = int(np.sqrt(2)*image_size + 0.5)
loss_fn = nn.MSELoss().cuda()
Supervised_model = UNet().cuda()
EI_model = UNet().cuda()
optimizer_Sup = torch.optim.Adam(Supervised_model.parameters(), lr=learning_rate, weight_decay=weight_dec)
optimizer_EI = torch.optim.Adam(EI_model.parameters(), lr=learning_rate, weight_decay=weight_dec)
scheduler_Sup = torch.optim.lr_scheduler.MultiStepLR(optimizer_Sup, milestones=[2000,3000,4000], gamma=0.2)
scheduler_EI = torch.optim.lr_scheduler.MultiStepLR(optimizer_EI, milestones=[2000,3000,4000], gamma=0.2)
Sup_psnrs_train,Sup_psnrs_test= [],[]
EI_psnrs_train,EI_psnrs_test= [],[]
gt_path = ('/content/drive/MyDrive/Final_year_project/src/Dataset/Groud_Truth_train.mat')
gt_path_test = ('/content/drive/MyDrive/Final_year_project/src/Dataset/Groud_Truth_test.mat')

dataloader_train,dataset_train=dataloader_train(gt_path,batch_size)
dataloader_test,dataset_test=dataloader_test(gt_path_test,batch_size)

EI_Model_path_0 = '/content/drive/MyDrive/Final_year_project/Trained_model/alpha_model/alpha_0.1'
EI_Model_path_1 = '/content/drive/MyDrive/Final_year_project/Trained_model/alpha_model/alpha_1'
EI_Model_path_10 = '/content/drive/MyDrive/Final_year_project/Trained_model/alpha_model/alpha_10'
EI_Model_path_100 = '/content/drive/MyDrive/Final_year_project/Trained_model/EI_model'
EI_Model_path_1000 = '/content/drive/MyDrive/Final_year_project/Trained_model/alpha_model/alpha_1000'
EI_psnr_0 = []
EI_psnr_1 = []
EI_psnr_10 = []
EI_psnr_100 = []
EI_psnr_1000 = []
EI_model_path = [EI_Model_path_0,EI_Model_path_1,EI_Model_path_10,EI_Model_path_100,EI_Model_path_1000]
EI_psnr = [EI_psnr_0,EI_psnr_1,EI_psnr_10,EI_psnr_100,EI_psnr_1000]
views=[10,30,50,70,90]
s = slice(40,49,1)
for j in range(0,5):
  for i in np.linspace(10,90,5, endpoint=True):
    EI_path = os.path.join(EI_model_path[j], '{}-views'.format(int(i)))
    n_views=int(i)
    angles = np.linspace(0, np.pi, n_views, endpoint=False)
    radon = Radon(image_size, angles, clip_to_circle=False, det_count=det_count)
    EI_psnrs_train,EI_psnrs_test = EI_test(dataloader_test, EI_path, loss_fn,radon,epochs)
    EI_psnrs_test=EI_psnrs_test[s]
    EI_psnr[j].append(np.mean(EI_psnrs_test))

  

plt.figure(figsize=(10,4))
plt.plot(views,EI_psnr_0,label="alpha=0.1")
plt.plot(views,EI_psnr_1,label="alpha=1")
plt.plot(views,EI_psnr_10,label="alpha=10")
plt.plot(views,EI_psnr_100,label="alpha=100")
plt.plot(views,EI_psnr_1000,label="alpha=1000")
plt.xlabel('Views')
# Set the y axis label of the current axis.
plt.ylabel('PSNR(dB)')
# Set a title of the current axes.
#plt.title('Two or more lines on same plot with suitable legends ')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.savefig('/content/drive/MyDrive/Final_year_project/Figures/EI_alpha')
plt.show()