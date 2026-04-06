import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from db import get_crashes

def run_q3():
    raw_crashes = get_crashes()
    plt.figure()

    month_order = [
        "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
    ]

    flag_cols = ["cyclist_flag", "heavy_veh_flag", "intersection_crash", "motorcycle_flag", "parked_vehicle_flag", "parking_lot_flag","pedestrian_flag" ]

    #to keep format consistent
    raw_crashes["month_of_year"] = raw_crashes["month_of_year"].str.strip().str.upper()



    # ##################################################################
    # # Top 10 Dangerous Roads for Pedestrians & Cyclists
    # ##################################################################

    ped_road_counts = (
        raw_crashes[raw_crashes['pedestrian_flag'] == 'Yes'].groupby('street_full_name').size()
    )

    cyc_road_counts = (
        raw_crashes[raw_crashes['cyclist_flag'] == 'Yes'].groupby('street_full_name').size()
    )

    top_roads_vulnerable = pd.DataFrame({
        'Pedestrians': ped_road_counts,
        'Cyclists': cyc_road_counts
    }).fillna(0)

    top_roads_vulnerable['Total'] = top_roads_vulnerable['Pedestrians'] + top_roads_vulnerable['Cyclists']
    top_roads_vulnerable = top_roads_vulnerable.sort_values(by='Total', ascending=False).head(10)


    top_roads_vulnerable[['Pedestrians', 'Cyclists']].plot(
        kind='barh', 
        stacked=True, 
        figsize=(12, 7), 
        color=["crimson", "navy"]
    )

    plt.title("Top 10 Most Dangerous Roads for Pedestrians & Cyclists")
    plt.xlabel("Number of Crashes")
    plt.ylabel("Road Name")
    plt.legend(title="User Type")
    plt.gca().invert_yaxis() 

    plt.subplots_adjust(left=0.3) #adjusting for long road names
    plt.savefig('output_figures/q3/Top 10 Most Dangerous Roads for Pedestrians & Cyclists.png')


    # ##################################################################
    # # time of day when cyclists/pedestrians are most vulnerable#
    # ##################################################################
    plt.figure()
    time_order = [
        '00:00-02:59', '03:00-05:59', '06:00-08:59', '09:00-11:59',
        '12:00-14:59', '15:00-17:59', '18:00-20:59', '21:00-23:59'
    ]

    ped_time_counts = (
        raw_crashes[raw_crashes['pedestrian_flag'] == 'Yes'].groupby('time_category').size()
    )

    cyc_time_counts = (
        raw_crashes[raw_crashes['cyclist_flag'] == 'Yes'].groupby('time_category').size()
    )

    time_vulnerability = pd.DataFrame({
        'Pedestrians': ped_time_counts,
        'Cyclists': cyc_time_counts
    }).fillna(0).reindex(time_order)

    time_vulnerability.plot(kind='bar', figsize=(10, 6), color=["crimson", "navy"])

    plt.title("Vulnerable Road User Crashes by Time")
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Crashes")
    plt.legend(title="User Type")
    plt.tight_layout()
    plt.savefig('output_figures/q3/Vulnerable Road User Crashes by Time.png')



    # ##################################################################
    # # Top 10 Dangerous Intersections for Pedestrians & Cyclists
    # ##################################################################
    plt.figure()
    #handling the 'nan' strings in cross street names
    def clean_intersection(row):
        main = str(row['street_full_name']).strip()
        cross = str(row['cross_street_full_name']).strip()
        
        #just to checkif cross street is empty
        if cross.lower() in ['nan', '', 'none', 'unknown']:
            cross = "Mid-Block"
            
        return f"{main} @ {cross}"

    raw_crashes['intersection_name'] = raw_crashes.apply(clean_intersection, axis=1)

    ped_counts = (
        raw_crashes[raw_crashes['pedestrian_flag'] == 'Yes'].groupby('intersection_name').size()
    )

    cyc_counts = (
        raw_crashes[raw_crashes['cyclist_flag'] == 'Yes'].groupby('intersection_name').size()
    )

    top_vulnerable = pd.DataFrame({
        'Pedestrians': ped_counts,
        'Cyclists': cyc_counts
    }).fillna(0) 

    top_vulnerable['Total'] = top_vulnerable['Pedestrians'] + top_vulnerable['Cyclists']
    top_vulnerable = top_vulnerable.sort_values(by='Total', ascending=False).head(10)


    top_vulnerable[['Pedestrians', 'Cyclists']].plot(
        kind='barh', 
        stacked=True, 
        figsize=(12, 7), 
        color=["crimson", "navy"]
    )

    plt.title("Top 10 Most Dangerous Intersections for Pedestrians & Cyclists")
    plt.xlabel("Number of Crashes")
    plt.ylabel("Intersection Location")
    plt.legend(title="User Type")
    plt.gca().invert_yaxis() #highest count at the top

    #adjusting layout of chart so long names like mid-block don't get cut off
    plt.subplots_adjust(left=0.35) 
    plt.savefig('output_figures/q3/Top 10 Most Dangerous Intersections for Pedestrians & Cyclists.png')



    # ##########################
    # # accident type vs total casualties#
    # ##########################
    plt.figure()
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
    plt.savefig('output_figures/q3/Total Number of Victims by Crash Type.png')



    # ##########################
    # # accident location (intersection and non-intersection) vs road users (pedestrians and cyclists)#
    # ##########################
    plt.figure()

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
    plt.savefig('output_figures/q3/Pedestrian & Cyclist Crashes Intersection vs Non-Intersection.png')



