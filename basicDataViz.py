import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def saveCorrMatrix(df,save_to_parquet=False):
    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(25, 20))
    cmap = sns.diverging_palette(300, 20, as_cmap=True)


    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=False, linewidths=0.1, cbar_kws={"shrink": .1}, ax = ax)
    plt.savefig("Viz/corrMatrix.png")
    if save_to_parquet:
        corr.to_parquet('df.parquet.gzip',compression='gzip')

def saveHistogram(df):
    fig, axs = plt.subplots(5,5,figsize=(30, 30) )
    columns = list(df.columns[:2])+list(df.columns[3:])
    for i in range(5):
        for j in range(5):
                axs[i,j].hist(df[columns[i*5+j]])
                axs[i,j].set_title(columns[i*5+j])   
    plt.savefig("Viz/hist.png")   

if __name__ == "__main__":
    try:
        os.mkdir("Viz")
        print("created Viz")
    except:
        print("Viz already present")
    path = "dataset/datasetcleaned.csv"
    if not os.path.isfile(path):
        os.system('python3 dataCleaning.py')
    df = pd.read_csv(path)
    saveCorrMatrix(df)
    saveHistogram(df)


