
import pandas as pd
import matplotlib.pyplot as plt
from db import get_crashes, get_filtered_populations,get_crashes_per_100k


raw_crashes = get_crashes()
raw_populations = get_filtered_populations()
crashes_per_100k = get_crashes_per_100k()

##########################
# crashes by municipality#
##########################
crashes_per_100k.sort_values("total_crashes", ascending=False).head(10).plot.bar( x="municipality", y = "total_crashes", color = ["blue"])
plt.xlabel("Municipality")
plt.ylabel("Total Crashes")
plt.title("Number of Crashes by Municipality (Top 10)")
plt.tight_layout()
plt.show()

#############################
# victims by municipality   #
#############################
crashes_per_100k.sort_values("total_victims", ascending=False).head(10).plot.bar( x="municipality", y = "total_victims", color = ["green"])
plt.xlabel("Municipality")
plt.ylabel("Number of Victims")
plt.title("Number of Victims by Municipality (Top 10)")
plt.tight_layout()
plt.show()

###############################
#municipalities by population #
###############################
fig, ax = plt.subplots(figsize=(10, 14))

raw_populations.sort_values("total", ascending=False).set_index("municipality").plot(kind="barh", color="purple", width=0.8, ax=ax)

ax.set_title("Populations by Municipality")
ax.set_xlabel("Population")
ax.tick_params(labelsize=8)

plt.subplots_adjust(left=0.35)
plt.tight_layout()
plt.show()

########################
# population histogram #
########################

fig, ax = plt.subplots(figsize=(6,8))
ax.boxplot(raw_populations["total"])
ax.set_title("Distribution of Municipality Populations")
ax.set_ylabel("Population")
ax.set_xticklabels([""])
plt.tight_layout()
plt.show()

###################################
# crashes per 100k by municipality#
###################################

crashes_per_100k.sort_values("crashes_per_100k", ascending=False).head(10).plot.bar( x="municipality", y = "crashes_per_100k", color = ["blue"])
plt.xlabel("Municipality")
plt.ylabel("Crashes per 100k")
plt.title("Rate of Crashes per 100k by Municipality (Top 10)")
plt.tight_layout()
plt.show()

crashes_per_100k.to_csv("output_tables/crashes_per_100k.csv", index=False)


####################################
# victims per 100k by municipality #
####################################
crashes_per_100k.sort_values("victims_per_100k", ascending=False).head(10).plot.bar( x="municipality", y = "victims_per_100k", color = ["green"])
plt.xlabel("Municipality")
plt.ylabel("Victims per 100k")
plt.title("Rate of Victims per 100k by Municipality (Top 10)")
plt.tight_layout()
plt.show()