import pandas as pd
import numpy as np

if __name__ == "__main__":
    print("Loading the data")
    df = pd.read_csv("dataset/train_test.csv")
    print("data loaded!")
    # One hot encoding
    df = df.join(pd.get_dummies(df['DEPARTING_AIRPORT']), lsuffix= 'DEP_' )
    df = df.join(pd.get_dummies(df['PREVIOUS_AIRPORT']), lsuffix= 'PREV_' )
    df = df.join(pd.get_dummies(df['DEP_BLOCK']))
    df = df.join(pd.get_dummies(df['CARRIER_NAME']))
    # Dropping old columns
    df = df.drop(['DEPARTING_AIRPORT', 'PREVIOUS_AIRPORT', 'CARRIER_NAME', 'DEP_BLOCK'], axis=1)

    print("data loaded!") 
    print("saving clean data")
    df.to_csv('dataset/datasetcleaned.csv')
    print("data saved!")
