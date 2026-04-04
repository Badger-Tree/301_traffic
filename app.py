import db

def main():
    def setup():
        #create the population and crash tables
        db.create_crash_table()
        db.import_crash_csv("Southern Interior_Full Data_data.csv")
        db.create_population_table()
        db.import_population_csv("Population_Projections.csv")


    def create_aggregations():
        # calculate crashes per 100k in each munipcipality
        db.create_crashes_join_population()
        
    def export_to_csv():
        db.export_crashes()
        db.export_population()
        db.export_crashes_join_population()
    setup()
    create_aggregations()
    export_to_csv()
    
if __name__ == "__main__":
    main()