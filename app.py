import db

def main():
    #create the population and crash tables
    # db.create_crash_table()
    # db.import_crash_csv("Southern Interior_Full Data_data.csv")
    # db.import_population_csv("Population_Projections.csv")

    
    # calculate crashes per 100k in each munipcipality
    db.create_regional_crash_summaries()
    db.create_crashes_per_100k()
    
if __name__ == "__main__":
    main()