import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_filtered_populations


raw_crashes = get_crashes()
#raw_populations = get_filtered_populations()
# ##################
# #crashes by flag #
# ##################
flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

# # melt flips the table around so each flag/outcome is a row
# # each row is now: flag, yes/no, count
# # count is the same, it's not aggregated yet 
# df_long = raw_crashes.melt(
#     id_vars="total_crashes",
#     value_vars=flag_cols,
#     var_name="flag",
#     value_name="value"
# )

# # aggregation
# # now the data is aggregated by flag type, yes/no, and sum of crashes
# # unstack moves the yes/no into separate columns so they can be charted ina bar chart
# # each row is now: flag, sum of yes, sum of no
# df_grouped = (
#     df_long.groupby(["flag", "value"])["total_crashes"]
#     .sum()
#     .unstack()
# )
# #this just flips the order of yes/no in stack because I thought it was more readable
# df_grouped = df_grouped[['Yes', 'No']]

# # Plot stacked bar
# df_grouped.plot(kind="bar", stacked=True,color=["blue", "lightgrey"])
# plt.title("Crashes by Flag (Yes vs No)")
# plt.ylabel("Total Crashes")
# plt.xlabel("Accident Flag")
# plt.tight_layout()
# plt.show()

# ## prints yes/no summary for each flag
# flag_dataframes = {}
# for col in flag_cols:
#     df = raw_crashes.groupby(col)["total_crashes"].sum().reset_index()
#     flag_dataframes[col] = df

# for col, df in flag_dataframes.items():
#     print(f"\nColumn: {col}")
#     print(df)
    
##################
#victims by flag #
##################
# flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

# df_long = raw_crashes.melt(
#     id_vars="total_victims",
#     value_vars=flag_cols,
#     var_name="flag",
#     value_name="value"
# )
# df_grouped = (
#     df_long.groupby(["flag", "value"])["total_victims"]
#     .sum()
#     .unstack()
# )
# #this just flips the order of yes/no in stack because I thought it was more readable
# df_grouped = df_grouped[['Yes', 'No']]

# # Plot stacked bar
# df_grouped.plot(kind="bar", stacked=True,color=["green", "lightgrey"])
# plt.title("Victims by Flag (Yes vs No)")
# plt.ylabel("Total Victims")
# plt.xlabel("Accident Flag")
# plt.tight_layout()
# plt.show()



# ################################
# #frequency of flags in crashes #
# ################################
# flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

# yes_counts = {
#     col: raw_crashes.loc[raw_crashes[col] == "Yes", "total_crashes"].sum()
#     for col in flag_cols
# }
# yes_series = pd.Series(yes_counts)

# yes_series.sort_values().plot(kind="bar", figsize=(8,5), color = ["blue"])

# plt.ylabel("Total Crashes")
# plt.title("Crashes by Flag (Yes Only)")
# plt.tight_layout()
# plt.show()

# ###################################
# #frequency of flags in casualties #
# ###################################
# flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

# yes_counts = {
#     col: raw_crashes.loc[raw_crashes[col] == "Yes", "total_victims"].sum()
#     for col in flag_cols
# }
# yes_series = pd.Series(yes_counts)

# yes_series.sort_values().plot(kind="bar", figsize=(8,5), color = ["green"])

# plt.ylabel("Total Victims")
# plt.title("Victims by Flag (Yes Only)")
# plt.tight_layout()
# plt.show()

# #################
# #crashes by day #
# #################

# raw_crashes["day_of_week"] = raw_crashes["day_of_week"].str.strip().str.title()

# day_order = [
#     "Monday",
#     "Tuesday",
#     "Wednesday",
#     "Thursday",
#     "Friday",
#     "Saturday",
#     "Sunday"
# ]

# crashes_by_day = raw_crashes.groupby("day_of_week")["total_crashes"].sum().reindex(day_order)
# crashes_by_day.plot(kind="bar", color = ["blue"])
# plt.title("Crashes by Day of the Week")
# plt.xlabel("Day")
# plt.ylabel("Number of Crashes")
# plt.tight_layout()
# plt.show()

# #################
# #victims by day #
# #################

# crashes_by_day = raw_crashes.groupby("day_of_week")["total_victims"].sum().reindex(day_order)
# crashes_by_day.plot(kind="bar",color = ["green"])
# plt.title("Victims by Day of the Week")
# plt.xlabel("Day")
# plt.ylabel("Number of Victims")
# plt.tight_layout()
# plt.show()

# ###################
# #crashes by month #
# ###################

# month_order = [
#     "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
# ]

# #counting crashes per month
# crashes_by_month = raw_crashes.groupby("month_of_year")["total_crashes"].sum().reindex(month_order, fill_value=0)

# #just made shorter labels for graph
# short_labels = [
#     "Jan","Feb","Mar","Apr","May","Jun",
#     "Jul","Aug","Sep","Oct","Nov","Dec"
# ]

# crashes_by_month.index = short_labels
# crashes_by_month.plot(kind="bar", color = ["blue"])
# plt.title("Crashes by Month")
# plt.xlabel("Month")
# plt.ylabel("Number of Crashes")
# plt.tight_layout()
# plt.show()


# ###################
# #victims by month #
# ###################

# month_order = [
#     "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
# ]

# #counting crashes per month
# victims_by_month = raw_crashes.groupby("month_of_year")["total_victims"].sum().reindex(month_order, fill_value=0)

# victims_by_month.index = short_labels
# victims_by_month.plot(kind="bar",color = ["green"])
# plt.title("Victims by Month")
# plt.xlabel("Month")
# plt.ylabel("Number of Victims")
# plt.tight_layout()
# plt.show()



###################
#crashes by time #
###################

time_order = [
    "00:00-02:59",
    "03:00-05:59",
    "06:00-08:59",
    "09:00-11:59",
    "12:00-14:59",
    "15:00-17:59",
    "18:00-20:59",
    "21:00-23:59"
]

crashes_by_time = raw_crashes.groupby("time_category")["total_crashes"].sum().reindex(time_order, fill_value=0)

crashes_by_time.index = time_order
crashes_by_time.plot(kind="bar",color = ["blue"])
plt.title("Crashes by Time of Day")
plt.xlabel("Time Category")
plt.ylabel("Number of Crashes")
plt.tight_layout()
plt.show()


##################
#victims by time #
##################

victims_by_time = raw_crashes.groupby("time_category")["total_victims"].sum().reindex(time_order, fill_value=0)

victims_by_time.index = time_order
victims_by_time.plot(kind="bar",color = ["green"])
plt.title("Victims by Time of Day")
plt.xlabel("Time Category")
plt.ylabel("Number of Victims")
plt.tight_layout()
plt.show()



month_order = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

#to keep format consistent
raw_crashes["month_of_year"] = raw_crashes["month_of_year"].str.strip().str.upper()



#######################
# crash type vs month #
#######################
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


################################
# accident type vs time of day #
################################


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


# #############################
# # crash type vs day of week #
# #############################

# day_order = [
#     "MONDAY",
#     "TUESDAY",
#     "WEDNESDAY",
#     "THURSDAY",
#     "FRIDAY",
#     "SATURDAY",
#     "SUNDAY"
# ]

# flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag", "pedestrian_flag", "animal_flag"]

# day_results = {}

# for flag in flag_cols:
#     counts = (
#         raw_crashes[raw_crashes[flag] == "Yes"].groupby("day_of_week").size().reindex(day_order, fill_value=0)
#     )
#     day_results[flag] = counts

# day_vs_type_df = pd.DataFrame(day_results)

# day_vs_type_df.plot(figsize=(10, 6), marker='o')

# plt.title("Crash Type vs Day of Week")
# plt.ylabel("Number of Crashes")
# plt.xlabel("")
# plt.xticks(range(len(day_order)), day_order)
# plt.tight_layout()
# plt.show()

