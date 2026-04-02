import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_populations, get_crashes_per_municipality,get_crashes_per_100k


raw_crashes = get_crashes()

print(raw_crashes.describe(include='all'))
# print(raw_crashes.head(5))

# print(f"shape: {raw_crashes.shape}")
# aggregated = raw_crashes.groupby(by="municipality_name")
# print(aggregated.head(10))


# crashes_per_municipality.sort_values("total_crashes", ascending=False).head(10).plot.bar( x="municipality_name", y = "total_crashes")
# plt.xlabel("Municipality")
# plt.ylabel("Number of Crashes")
# plt.title("Crashes per Municipality")
# plt.show()

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

crashes_by_day = raw_crashes.groupby("day_of_week")["total_crashes"].sum().reindex(day_order)

crashes_by_day.plot(kind="bar")

plt.title("Crashes by Day of the Week")
plt.xlabel("Day")
plt.ylabel("Number of Crashes")

plt.tight_layout()

plt.show()


#crashes by month
month_order = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

#counting crashes per month
crashes_by_month = raw_crashes.groupby("month_of_year")["total_crashes"].sum().reindex(month_order, fill_value=0)

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


