import db

def main():
    db.create_crash_table()
    db.import_crash_csv('Southern Interior_Full Data_data.csv')
    
    db.import_population_csv('Population_Projections.csv')
    
    print("Crash data:", db.get_crashes())
    print("Population data:", db.get_population())

if __name__ == "__main__":
    main()