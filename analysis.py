import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_populations, get_crashes_per_municipality,get_crashes_per_100k


############################
# exploratory data analysis#
############################ 

raw_crashes = get_crashes()

print(raw_crashes.shape)

def get_summmary(df):
    """gets summary info for each column"""
    summary_data = []    
    for col in df.columns:
        col_dtype = df[col].dtype
        num_nulls = df[col].isnull().sum()
        num_non_nulls = df[col].notnull().sum()
        num_distinct_values = df[col].nunique()
        summary_data.append({
            'column_name': col,
            'column_dtype': col_dtype,
            'num_nulls': num_nulls,
            'num_non_nulls': num_non_nulls,
            'num_of_distinct_values': num_distinct_values}
        )
    return summary_data
summary_df = pd.DataFrame(get_summmary(raw_crashes))
print(summary_df)
