# config.py

from dataclasses import dataclass

@dataclass
class Config:

    # Data params
    PATH_FILES_BONOBO: str = 'your_path' #'
    PATH_LUT_BONOBO: str = 'your_path' #'lut_labelled_20230628.csv'
    PATH_CONTINOUS_EEG: str = 'your_path/continuousEEG'

    FQ: int = 128 # Hz
    
    
    # Preprocessing 
    MONTAGE: str = 'conbine'
    WINDOWSIZE: float = 1 # 2 seconds
    
	# Model parameters
    N_CHANNELS: int = 37 #19+18

    # training parameters
    BATCH_SIZE: int = 256 #test 128
    LR: float = 1e-4 #test 1e-4

    def print_config(self):
        print('THIS CONFIG FILE CONTAINS THE FOLLOWING PARAMETERS :\n')
        for key, value in self.__dict__.items():
            print(key, value)