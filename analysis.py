import pandas as pd
from db import get_crashes, get_populations, get_crashes_per_municipality,get_crashes_per_100k


raw_crashes = get_crashes()
populations = get_populations()
crashes_per_municipality = get_crashes_per_municipality()
crashes_per_100k = get_crashes_per_100k()
# head methods to see if they work, not important
# print(raw_crashes.head())
# print(populations.head())
# print(crashes_per_municipality.head())
# print(crashes_per_100k.head())



