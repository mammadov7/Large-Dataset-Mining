import pandas as pd

path = "assets/aggregated_data.parquet"
flight_df = pd.read_parquet(path).reset_index()
