import pandas as pd
import numpy as np

if __name__ == "__main__":
    print("Loading the data")
    df = pd.read_csv("dataset/train_test.csv.zip")
    print("data loaded!")
    # One hot encoding
    df = pd.get_dummies(df, columns=['DEPARTING_AIRPORT', 'PREVIOUS_AIRPORT', 'DEP_BLOCK', 'CARRIER_NAME'], sparse=True)
    print("saving clean data")
    df.to_csv('dataset/datasetcleaned.csv.zip', compression = 'zip') 
    print("data saved!")
