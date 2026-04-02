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

crashes_per_municipality = get_crashes_per_municipality()
crashes_per_municipality.sort_values("total_crashes", ascending=False).head(10).plot.bar( x="municipality_name", y = "total_crashes")
plt.xlabel("Municipality")
plt.ylabel("Number of Crashes")
plt.title("Crashes per Municipality")
plt.show()

#crashes by day

raw_crashes["day_of_week"] = raw_crashes["day_of_week"].str.strip().str.title()

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

crashes_by_day = raw_crashes["day_of_week"].value_counts().reindex(day_order)

crashes_by_day.plot(kind="bar")

plt.title("Crashes by Day of the Week")
plt.xlabel("Day")
plt.ylabel("Number of Crashes")

plt.tight_layout()

plt.show()


#crashes by month
month_order = {
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
}

#counting crashes per month
crashes_by_month = raw_crashes["month_of_year"].value_counts().reindex(month_order, fill_value=0)

#just made shorter labels for graph
short_labels = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

crashes_by_month.index = short_labels

crashes_by_month.plot(kind="bar")

plt.title("Crashes by Month")
plt.xlabel("Month")
plt.ylabel("Number of Crashes")

plt.tight_layout()

plt.show()