import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_populations, get_crashes_join_population


raw_crashes = get_crashes()
raw_populations = get_populations()
crashes_join_population = get_crashes_join_population()
############################
# exploratory data analysis#
############################ 

########################
# data summary crashes #
########################
print(raw_crashes.shape)

def get_summmary(df):
    """gets summary info for each column"""
    summary_data = []    
    for col in df.columns:
        col_dtype = df[col].dtype
        num_nulls = df[col].isnull().sum()
        num_non_nulls = df[col].notnull().sum()
        num_distinct_values = df[col].nunique()
        num_empty_strings = (df[col] == '').sum()
        summary_data.append({
            'column_name': col,
            'column_dtype': col_dtype,
            'num_nulls': num_nulls,
            'num_non_nulls': num_non_nulls,
            'num_of_distinct_values': num_distinct_values,
            'num_empty_strings' : num_empty_strings
            }
        )
    return summary_data
summary_crash_df = pd.DataFrame(get_summmary(raw_crashes))
print(summary_crash_df)

###########################
# data summary population #
###########################
print(raw_populations.shape)
pop_mean = raw_populations["total"].mean()

pop_summary = raw_populations["total"].describe().to_frame().T
pop_summary = pop_summary.rename(index={"total": "Population"})
pop_summary = pop_summary.round(0)


print(f"mean: {pop_mean}")
print(f"summary: {pop_summary}")

summary_population_df = pd.DataFrame(get_summmary(raw_populations))
print(summary_population_df)

###########################
# crashes_join_population #
###########################
summary_crashes_join_population_df = pd.DataFrame(get_summmary(crashes_join_population))
print(summary_crashes_join_population_df)