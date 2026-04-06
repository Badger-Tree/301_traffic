import db, analysis_eda as eda, analysis_q1 as q1, analysis_q2 as q2, analysis_q3 as q3, analysis_q4 as q4

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
    def run_analysis():
        eda.run_eda()
        q1.run_q1()
        q2.run_q2()
        q3.run_q3()
        q4.run_q4()
    
    setup()
    create_aggregations()
    export_to_csv()
    run_analysis()
    
    
    
if __name__ == "__main__":
    main()