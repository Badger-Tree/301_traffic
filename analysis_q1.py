
import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_filtered_populations,get_crashes_per_100k


raw_crashes = get_crashes()
raw_populations = get_filtered_populations()
crashes_per_100k = get_crashes_per_100k()

# ##########################
# # crashes by municipality#
# ##########################
# crashes_per_100k.sort_values("total_crashes", ascending=False).head(10).plot.bar( x="municipality", y = "total_crashes", color = ["blue"])
# plt.xlabel("Municipality")
# plt.ylabel("Total Crashes")
# plt.title("Number of Crashes by Municipality (Top 10)")
# plt.tight_layout()
# plt.show()

# #############################
# # victims by municipality   #
# #############################
# crashes_per_100k.sort_values("total_victims", ascending=False).head(10).plot.bar( x="municipality", y = "total_victims", color = ["green"])
# plt.xlabel("Municipality")
# plt.ylabel("Number of Victims")
# plt.title("Number of Victims by Municipality (Top 10)")
# plt.tight_layout()
# plt.show()

# ###############################
# #municipalities by population #
# ###############################
# fig, ax = plt.subplots(figsize=(10, 14))

# raw_populations.sort_values("total", ascending=False).set_index("municipality").plot(kind="barh", color="purple", width=0.8, ax=ax)

# ax.set_title("Populations by Municipality")
# ax.set_xlabel("Population")
# ax.tick_params(labelsize=8)

# plt.subplots_adjust(left=0.35)
# plt.tight_layout()
# plt.show()

# ########################
# # population histogram #
# ########################

# fig, ax = plt.subplots(figsize=(6,8))
# ax.boxplot(raw_populations["total"])
# ax.set_title("Distribution of Municipality Populations")
# ax.set_ylabel("Population")
# ax.set_xticklabels([""])
# plt.tight_layout()
# plt.show()

# ###################################
# # crashes per 100k by municipality#
# ###################################

# crashes_per_100k.sort_values("crashes_per_100k", ascending=False).head(10).plot.bar( x="municipality", y = "crashes_per_100k", color = ["blue"])
# plt.xlabel("Municipality")
# plt.ylabel("Crashes per 100k")
# plt.title("Rate of Crashes per 100k by Municipality (Top 10)")
# plt.tight_layout()
# plt.show()


# ####################################
# # victims per 100k by municipality #
# ####################################
# crashes_per_100k.sort_values("victims_per_100k", ascending=False).head(10).plot.bar( x="municipality", y = "victims_per_100k", color = ["green"])
# plt.xlabel("Municipality")
# plt.ylabel("Victims per 100k")
# plt.title("Rate of Victims per 100k by Municipality (Top 10)")
# plt.tight_layout()
# plt.show()

###########################
# population vs accidents #
 ##########################

fig, ax = plt.subplots()
crashes_per_100k.plot.scatter(
    x="population",
    y="total_crashes",
    ax=ax
)

municipalities_to_label = ["KELOWNA", "KAMLOOPS", "VERNON", "LYTTON"]
offsets = [(-50,-20), (2,10), (5,15), (10,-15)]
offset_map = dict(zip(municipalities_to_label, offsets))

labelled_municipalities = crashes_per_100k[crashes_per_100k["municipality"].isin(municipalities_to_label)]
for _, row in labelled_municipalities.iterrows():
    dx, dy = offset_map[row["municipality"]]
    
    ax.annotate(
        row["municipality"],
        (row["population"], row["total_crashes"]),
        xytext=(dx, dy),
        textcoords="offset points",
        arrowprops=dict(arrowstyle='->')
    )

ax.set_xlabel("Population")
ax.set_ylabel("Crashes")
ax.set_title("Crashes vs Population")
plt.tight_layout()
plt.show()

##################################
# population vs rate of accident #
##################################

fig, ax = plt.subplots()

crashes_per_100k.plot.scatter(
    x="population",
    y="crashes_per_100k",
    ax=ax
)

municipalities_to_label = ["KELOWNA", "KAMLOOPS", "VERNON", "LYTTON", "CACHE CREEK","PRINCETON"]
labelled_municipalities = crashes_per_100k[crashes_per_100k["municipality"].isin(municipalities_to_label)]
for _, row in labelled_municipalities.iterrows():
    ax.annotate(
        row["municipality"],
        (row["population"], row["crashes_per_100k"]),
        xytext=(1,1),
        textcoords="offset points",
        arrowprops=None
    )

ax.set_xlabel("Population")
ax.set_ylabel("Crashes per 100k")
ax.set_title("Crash Rates vs Population")

plt.tight_layout()
plt.show()