import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from db import get_crashes, get_populations, get_crashes_per_municipality,get_crashes_per_100k


raw_crashes = get_crashes()

month_order = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

#to keep format consistent
raw_crashes["month_of_year"] = raw_crashes["month_of_year"].str.strip().str.upper()



# ##########################
# # crash type vs month #
# ##########################
results = {}

for flag in flag_cols:
    counts = (
        raw_crashes[raw_crashes[flag] == "Yes"].groupby("month_of_year").size().reindex(month_order, fill_value=0)
    )

    results[flag] = counts

crash_type_vs_month = pd.DataFrame(results)
crash_type_vs_month.plot()

plt.title("Crash Type vs Month")
plt.xlabel("Month")
plt.ylabel("Number of Crashes")
plt.tight_layout()
plt.show()


# ##########################
# # accident type vs time of day#
# ##########################


time_order = sorted(raw_crashes["time_category"].unique())

flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag", "pedestrian_flag", "animal_flag"]

time_results = {}

for flag in flag_cols:
    counts = (
        raw_crashes[raw_crashes[flag] == "Yes"].groupby("time_category").size().reindex(time_order, fill_value=0)
    )
    time_results[flag] = counts

time_vs_type_df = pd.DataFrame(time_results)

time_vs_type_df.plot(figsize=(10, 6), marker='o')

plt.title("Crash Type vs Time of Day (3-Hr Blocks)")
plt.xlabel("Time Range")
plt.ylabel("Number of Crashes")
plt.xticks(range(len(time_order)), time_order)
plt.tight_layout()
plt.show()



# ##########################
# # crash severity (property dmg + casualty crash) vs month#
# ##########################

severity_vs_month = (
    raw_crashes.groupby(["month_of_year", "crash_severity"]).size().unstack().reindex(month_order)
)

severity_vs_month.plot()

plt.title("Crash Severity vs Month")
plt.xlabel("Month")
plt.ylabel("Number of Crashes")

plt.tight_layout()
plt.show()