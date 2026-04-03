import db

def main():
    def setup():
        #create the population and crash tables
        db.create_crash_table()
        db.import_crash_csv("Southern Interior_Full Data_data.csv")
        db.import_population_csv("Population_Projections.csv")
        db.create_refined_population()

    def create_aggregations():
        # calculate crashes per 100k in each munipcipality
        db.create_crashes_per_100k()
        
    
    setup()
    create_aggregations()
    
if __name__ == "__main__":
    main()