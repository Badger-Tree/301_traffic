import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from db import get_crashes


raw_crashes = get_crashes()

month_order = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

#to keep format consistent
raw_crashes["month_of_year"] = raw_crashes["month_of_year"].str.strip().str.upper()


# ################################
# #top 10 deadliest intersections#
# ################################

raw_crashes['intersection_name'] = raw_crashes['street_full_name'] + " @ " + raw_crashes['cross_street_full_name']

top_intersections = (
    raw_crashes[raw_crashes['intersection_crash'] == 'Yes'].groupby('intersection_name').size().sort_values(ascending=False).head(10)
)

top_intersections.plot(kind='barh', color='crimson', figsize=(10, 6))
plt.title("Top 10 Most Dangerous Intersections")
plt.xlabel("Number of Crashes")
plt.ylabel("Intersection")
plt.gca().invert_yaxis() #first spot at the top
plt.tight_layout()
plt.savefig('output_figures/q4/Top 10 Most Dangerous Intersections.png')




# ##########################
# # top 10 dangerous roads by total victims#
# ##########################

top_roads = (
    raw_crashes.groupby('street_full_name')['total_victims'].sum().sort_values(ascending=False).head(10)
)

plt.figure(figsize=(10, 6))
top_roads.plot(kind='barh', color="crimson")
plt.title("Top 10 Deadliest Roads (Total Victim Count)")
plt.xlabel("Total Number of Victims")
plt.ylabel("Road Name")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('output_figures/q4/Top 10 Deadliest Roads (Total Victim Count).png')




# ##########################
# # community profile (casualty vs property dmg); which communities have highest proportion of dangerous crashes#
# ##########################

comm_severity = (
    raw_crashes.groupby(['municipality', 'crash_severity']).size().unstack(fill_value=0)
)


comm_severity = comm_severity.sort_values(by='CASUALTY CRASH', ascending=False).head(10)

comm_severity.plot(kind='bar', stacked=True, figsize=(10, 6), color=["crimson", "grey"])
plt.title("Top 10 Communities by Crash Severity")
plt.xlabel("Municipality")
plt.ylabel("Number of Crashes")
plt.legend(title="Severity Type")
plt.tight_layout()
plt.savefig('output_figures/q4/Top 10 Communities by Crash Severity.png')

