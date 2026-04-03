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
# # accident type vs total casualties#
# ##########################

casualty_df = raw_crashes[raw_crashes["total_victims"] > 0]

casualty_sums = {}
for flag in flag_cols:
    total_for_type = casualty_df[casualty_df[flag] == "Yes"]["total_victims"].sum()
    clean_label = flag.replace("_flag", "").replace("_", " ").title()
    casualty_sums[clean_label] = total_for_type

casualty_analysis = pd.DataFrame.from_dict(
    casualty_sums, orient="index", columns=["Total Victims"]
).sort_values(by="Total Victims", ascending=False)

casualty_analysis.plot(kind="bar", color="crimson", legend=False)

plt.title("Total Number of Victims by Crash Type")
plt.xlabel("Crash Category")
plt.ylabel("Total Number of People")
plt.tight_layout()
plt.show()



# ##########################
# # accident location (intersection and non-intersection) vs road users (pedestrians and cyclists)#
# ##########################


raw_crashes['location_label'] = raw_crashes['intersection_crash'].map({
    'Yes': 'Intersection',
    'No': 'Non-Intersection'
})

ped_location = (
    raw_crashes[raw_crashes['pedestrian_flag'] == 'Yes']
    .groupby('location_label')
    .size()
)

cyc_location = (
    raw_crashes[raw_crashes['cyclist_flag'] == 'Yes']
    .groupby('location_label')
    .size()
)

location_comparison = pd.DataFrame({
    'Pedestrians': ped_location,
    'Cyclists': cyc_location
})

location_comparison.plot(kind='bar', figsize=(10, 6), color=["crimson","navy"])

plt.title("Pedestrian & Cyclist Crashes: Intersection vs. Non-Intersection")
plt.xlabel("Accident Location")
plt.ylabel("Number of Crashes")
plt.legend(title="User Type")
plt.tight_layout()
plt.show()




# ##########################
# # crash config vs severity#
# ##########################

config_severity = (
    raw_crashes.groupby(['derived_crash_config', 'crash_severity'])
    .size()
    .unstack(fill_value=0)
)

#claculating total col to sort bars by volume
config_severity['Total'] = config_severity.sum(axis=1)
config_severity = config_severity.sort_values(by='Total', ascending=True)

#then dropping total col so it doesn't plot as a bar
plot_data = config_severity.drop(columns=['Total'])

plot_data.plot(kind='barh', stacked=True, figsize=(10, 6), color=["navy", "crimson"])

plt.title("Crash Configuration vs. Severity")
plt.xlabel("Number of Crashes")
plt.ylabel("Derived Crash Configuration")
plt.legend(title="Severity", loc='lower right')
plt.tight_layout()
plt.show()



