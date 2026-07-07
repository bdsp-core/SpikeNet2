# SpikeNet2


This is the official implementation of our paper "Expert-Level Detection of Epilepsy Markers in EEG on Short and Long Timescales".


## Dependencies

To clone all files:


```
git clone https://github.com/bdsp-core/SpikeNet2.git
```



To install Python dependencies:


```
conda create -n SpikeNet2 python=3.10
conda activate SpikeNet2
pip install -r requirements.txt
```



## Data 

You can find the data here:  [Spikenet-2](https://bdsp.io/content/spikenet/2.0/)

## Model weights

The trained model checkpoints are hosted with the dataset on S3 (credentialed access via the bdsp.io project above):

```
s3://bdsp-opendata-restricted/spikenet2/Models/new_weights.ckpt                     # final model
s3://bdsp-opendata-restricted/spikenet2/Models/1s-round11-hardmine-chan_weights-v1.ckpt
```

Download `new_weights.ckpt` and point the checkpoint path in the prediction/localization notebooks at it. (Weights are not committed to git.)

## Reproduce

See [`REPRODUCE.md`](REPRODUCE.md) and [`DATA_SOURCE.md`](DATA_SOURCE.md).

- **Localization figure/results — no download needed (verified 2026-07-07).** `2_localization.ipynb` regenerates the spike-localization figure and per-class AUCs (0.91 / 0.85 / 0.83 / 0.81) directly from the committed `conbine_localization_predictions.csv`.
- **Full pipeline (detection figures, e.g. ROC):** download the EEG data + `new_weights.ckpt`, run `1_calculate_local_predictions.ipynb` / `prediction.ipynb` → `predictions.csv` → figures.

## Preparation

First, you need to download the EEG data above. Then run the jupyter notebook to transfer the '.mat' files into '.npy' files.

```
transfer_data.ipynb
```

Next, configure your file '/sleeplib/config.py'. Fill in your path into 'your_path'.

## Running Training

Run the following command to perform initial training of SpikeNet2.  

```
python train_initial_model.py
```


After we get the initial model,  it can be performed on control EEG dataset and get thousands of hard negative samples. Run the following command to perform the model on control EEG and get the predictions of EEG.

```
python continurous.py
```



Next, to get thousands of hard negative samples, we can run the code to get them.

```
hard_mining.ipynb
```



Then we get the new samples to run another round of hard mining.

```
python train_hard_model.py
```



If you want to check the model performance, please run the code

```
prediction.ipynb
```



## Citation
If you found our work useful in your research, please consider citing our works at:
> ```
>@article{li2025expert,
>  title={Expert-Level Detection of Epilepsy Markers in EEG on Short and Long Timescales},
>  author={Li, Jun and Goldenholz, Daniel M and Alkofer, Moritz and Sun, Chenxi and Nascimento, Fabio A and Halford, Jonathan J and Dean, Brian C and Galanti, Mattia and Struck, Aaron F and Greenblatt, Adam S and others},
>  journal={NEJM AI},
>  volume={2},
>  number={7},
>  pages={AIoa2401221},
>  year={2025},
>  publisher={Massachusetts Medical Society}
>}
> ```
