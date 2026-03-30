import db

def main():
    #create the population and crash tables
    db.create_crash_table()
    db.import_crash_csv('301_traffic\Southern Interior_Full Data_data.csv')
    
    db.import_population_csv('301_traffic\Population_Projections.csv')

    
    # calculate crashes per 100k in each munipcipality
    db.create_crashes_per_100k()
    
    print("Crash data:", db.get_crashes())
    print()
    print("Population data:", db.get_population())
    print()
    print("per 100k:", db.get_crashes_per_100k())
    print()
if __name__ == "__main__":
    main()