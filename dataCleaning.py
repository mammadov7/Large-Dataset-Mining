import pandas as pd
import numpy as np

if __name__ == "__main__":
    print("Loading the data")
    df = pd.read_csv("dataset/train_test_small.csv")
    df['DEP_BLOCK'] = pd.Categorical(df.DEP_BLOCK).codes
    df['CARRIER_NAME'] = pd.Categorical(df.CARRIER_NAME).codes
    df['DEPARTING_AIRPORT'] = pd.Categorical(df.DEPARTING_AIRPORT).codes
    df['PREVIOUS_AIRPORT'] = pd.Categorical(df.DEP_BLOCK).codes
    cols = ['DAY_OF_WEEK', 'DISTANCE_GROUP', 'DEP_BLOCK','SEGMENT_NUMBER', 'CONCURRENT_FLIGHTS', 'NUMBER_OF_SEATS',
        'CARRIER_NAME', 'AIRPORT_FLIGHTS_MONTH', 'AIRLINE_FLIGHTS_MONTH', 'AIRLINE_AIRPORT_FLIGHTS_MONTH', 
        'AVG_MONTHLY_PASS_AIRPORT', 'AVG_MONTHLY_PASS_AIRLINE', 'FLT_ATTENDANTS_PER_PASS', 'GROUND_SERV_PER_PASS',
        'PLANE_AGE', 'DEPARTING_AIRPORT', 'LATITUDE', 'PREVIOUS_AIRPORT', 'PRCP', 'SNOW', 'SNWD', 'AWND']
    print("data loaded!")
    print("saving clean data")
    df.to_csv('dataset/datasetcleaned.csv')
    print("data saved!")