import pandas as pd
import wandb
import torch
import os
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader
from torchvision import transforms
import torch
# load own code
import sys
sys.path.append('../')
from sleeplib.Resnet_15.model import FineTuning
from sleeplib.datasets import BonoboDataset , ContinousToSnippetDataset
from sleeplib.montages import CDAC_combine_montage
from sleeplib.transforms import cut_and_jitter,channel_flip, extremes_remover
# this holds all the configuration parameters
from sleeplib.config import Config
import pickle

# define model name and path
model_path = '/run/media/exx/Expansion2/code/Spike_37chan/Models/YOUR_MODEL_NAME'
# load config and show all default parameters
config = Config()
config.print_config()
# the config can be changed by setting config.PARAMETER = VALUE

# save config to model_path using pickle


combine_montage = CDAC_combine_montage()

# load dataset
df = pd.read_csv(config.PATH_LUT_BONOBO,sep=';') # ; -> ,
# add transformations
transform_train = transforms.Compose([cut_and_jitter(windowsize=config.WINDOWSIZE,max_offset=0.1,Fq=config.FQ), 
                                      channel_flip(p=0.5),
                                      extremes_remover(signal_max = 2000, signal_min = 20)
                                      ])
transform_val = transforms.Compose([cut_and_jitter(windowsize=config.WINDOWSIZE,max_offset=0,Fq=config.FQ),
                                    extremes_remover(signal_max = 2000, signal_min = 20)])#,CDAC_signal_flip(p=0)])


# init datasets
sub_df = df[df['total_votes_received']>2]
train_df = sub_df[sub_df['Mode']=='Train']
val_df = sub_df[sub_df['Mode']=='Val']

# set up dataloaders


Bonobo_train = BonoboDataset(train_df, 
                             config.PATH_FILES_BONOBO, 
                             transform=transform_train,
                             montage = combine_montage
                            )
train_dataloader = DataLoader(Bonobo_train, batch_size=config.BATCH_SIZE, shuffle=True, num_workers=os.cpu_count())

Bonobo_val = BonoboDataset(val_df, 
                           config.PATH_FILES_BONOBO, 
                           transform=transform_val, 
                           montage = combine_montage
                          )
val_dataloader = DataLoader(Bonobo_val, batch_size=config.BATCH_SIZE,shuffle=False,num_workers=os.cpu_count())



#Bonobo_con = ContinousToSnippetDataset('/home/ubuntu/data/Bonobo01742_0.mat',montage=montage)#montage use numpy,so .mat maybe cannot do it
#con_dataloader = DataLoader(Bonobo_con, batch_size=config.BATCH_SIZE,shuffle=False,num_workers=os.cpu_count())


#for i in range(5):
# build model
model = FineTuning(lr=config.LR,
                    head_dropout=config.HEAD_DROPOUT,
                    n_channels=config.N_CHANNELS,
                    n_fft=config.N_FFT,
                    hop_length=config.HOP_LENGTH)

# create a logger
wandb.init(dir='logging')
wandb_logger = WandbLogger(project='super_awesome_project') 

# create callbacks with early stopping and model checkpoint (saves the best model)
#callbacks = [EarlyStopping(monitor='val_loss',patience=5),ModelCheckpoint(dirpath=model_path,filename='weights',monitor='val_loss')]
callbacks = [ModelCheckpoint(dirpath=model_path, filename='37chan_weights', monitor='val_loss')]
# create trainer, use fast dev run to test the code
trainer = pl.Trainer(devices=1, accelerator="gpu", min_epochs=5,max_epochs=50,logger=wandb_logger,callbacks=callbacks,fast_dev_run=False)
# train the model
trainer.fit(model,train_dataloader,val_dataloader)
wandb.finish()
