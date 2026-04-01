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

