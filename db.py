import sqlite3
import csv
import pandas as pd

DB_NAME = 'database.db'  # your SQLite database file

# Connection Helper
def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(DB_NAME)

# Crash Table
def create_crash_table():
    """Create the crashes table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS crashes")
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS crashes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_of_loss_year INTEGER,
                    crash_severity TEXT,
                    cyclist_flag TEXT,
                    day_of_week TEXT,
                    derived_crash_config TEXT,
                    heavy_veh_flag TEXT,
                    intersection_crash TEXT,
                    month_of_year INTEGER,
                    motorcycle_flag TEXT,
                    parked_vehicle_flag TEXT,
                    parking_lot_flag TEXT,
                    pedestrian_flag TEXT,
                    region TEXT,
                    time_category TEXT,
                    municipality TEXT,
                    road_location_description TEXT,
                    street_full_name TEXT,
                    total_crashes INTEGER,
                    total_victims INTEGER,
                    animal_flag TEXT,
                    cross_street_full_name TEXT,
                    latitude REAL,
                    longitude REAL,
                    mid_block_crash TEXT
                )
            """)
            
    conn.commit()
    conn.close()

def import_crash_csv(file_path):
    """Import data from a CSV file into the crashes table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            total_crashes = int(row['Total Crashes']) if row['Total Crashes'] else None
            total_victims = int(row['Total Victims']) if row['Total Victims'] else None
            latitude = float(row['Latitude']) if row['Latitude'] else None
            longitude = float(row['Longitude']) if row['Longitude'] else None

            cursor.execute('''
                INSERT INTO crashes (
                    date_of_loss_year,
                    crash_severity,
                    cyclist_flag,
                    day_of_week,
                    derived_crash_config,
                    heavy_veh_flag,
                    intersection_crash,
                    month_of_year,
                    motorcycle_flag,
                    parked_vehicle_flag,
                    parking_lot_flag,
                    pedestrian_flag,
                    region,
                    time_category,
                    municipality,
                    road_location_description,
                    street_full_name,
                    total_crashes,
                    total_victims,
                    animal_flag,
                    cross_street_full_name,
                    latitude,
                    longitude,
                    mid_block_crash
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', [
                row['Date Of Loss Year'],
                row['Crash Severity'], 
                row['Cyclist Flag'], 
                row['Day Of Week'],
                row['Derived Crash Configuration'], 
                row['Heavy Veh Flag'],
                row['Intersection Crash'], 
                row['Month Of Year'], 
                row['Motorcycle Flag'],
                row['Parked Vehicle Flag'], 
                row['Parking Lot Flag'],
                row['Pedestrian Flag'], 
                row['Region'], 
                row['Time Category'], 
                row['Municipality Name'], 
                row['Road Location Description'],
                row['Street Full Name'], 
                total_crashes,
                total_victims, 
                row['Animal Flag'],
                row['Cross Street Full Name'],
                latitude, 
                longitude,
                row['Mid Block Crash']   
            ])
    
    conn.commit()
    conn.close()

# return crash table
def get_crashes():
    """this method returns the crashes table as a dataframe"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM crashes", conn)
    conn.close()
    return df


# Population Table
def create_population_table():
    """Create the population table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS population")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS population (
                        region TEXT,
                        municipality TEXT,
                        total INTEGER
                    )
                    """)
    
    conn.commit()
    conn.close()
    
def import_population_csv(file_path):
    """Import population data from CSV into the population table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    create_population_table()  # ensure table exists
    
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip first 6 metadata rows
        for _ in range(6):
            next(reader)
        
        # Skip header row
        headers = next(reader)
        
        for row in reader:
            region = row[0].strip()
            municipality = row[1].strip().upper()
            total = int(row[5].replace(',', '').strip()) #this is to take the comma out of the popularion field so it can be an integer
            cursor.execute('''
                INSERT INTO population (region, municipality, total)
                VALUES (?, ?, ?)
            ''', [region, municipality, total])
    
    conn.commit()
    conn.close()
    
# return population table
def get_populations():
    """this method returns the population table as a dataframe"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM population", conn)
    conn.close()
    return df

def create_regional_crash_summaries():
    """calculate summaries of crash data according to municipality"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS crashes_per_municipality")
    cursor.execute('''
                   CREATE TABLE crashes_per_municipality AS
                    SELECT 
                        c.municipality,
                        COUNT(*) AS total_crashes,
                        SUM(CASE WHEN c.crash_severity = 'CASUALTY CRASH' THEN 1 ELSE 0 END) AS casualty_accident_counts,
                        SUM(CASE WHEN c.animal_flag = 'Yes' THEN 1 ELSE 0 END) AS animal_flag_yes_count,
                        SUM(CASE WHEN c.cyclist_flag = 'Yes' THEN 1 ELSE 0 END) AS cyclist_flag_yes_count,
                        SUM(CASE WHEN c.heavy_veh_flag = 'Yes' THEN 1 ELSE 0 END) AS heavy_veh_flag_yes_count,
                        SUM(CASE WHEN c.intersection_crash = 'Yes' THEN 1 ELSE 0 END) AS intersection_crash_count,                        
                        SUM(CASE WHEN c.motorcycle_flag = 'Yes' THEN 1 ELSE 0 END) AS motorcycle_flag_yes_count,  
                        SUM(CASE WHEN c.parked_vehicle_flag = 'Yes' THEN 1 ELSE 0 END) AS parked_vehicle_flag_yes_count,
                        SUM(CASE WHEN c.parking_lot_flag = 'Yes' THEN 1 ELSE 0 END) AS parking_lot_flag_yes_count,
                        SUM(CASE WHEN c.pedestrian_flag = 'Yes' THEN 1 ELSE 0 END) AS pedestrian_flag_yes_count,
                        AVG(total_victims) as average_victims                       
                    FROM crashes AS c
                    GROUP BY c.municipality''')
    
    conn.commit()
    conn.close()
    
def get_crashes_per_municipality():
    """this method returns the crash data aggregated by municipality as a dataframe"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM crashes_per_municipality", conn)
    conn.close()
    return df

# calculate municipal crashes
def create_crashes_per_100k():
    """calculate crashes per 100k in each municipality"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS crashes_per_100k")
    cursor.execute("""
                   CREATE TABLE crashes_per_100k AS
                    SELECT 
                        c.municipality,
                        COUNT(*) AS total_crashes,
                        SUM(CASE WHEN c.crash_severity = 'CASUALTY CRASH' THEN 1 ELSE 0 END)* 100000.0 / p.total AS casualty_accident_counts,
                        SUM(CASE WHEN c.animal_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS animal_flag_yes_count,
                        SUM(CASE WHEN c.cyclist_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS cyclist_flag_yes_count,
                        SUM(CASE WHEN c.heavy_veh_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS heavy_veh_flag_yes_count,
                        SUM(CASE WHEN c.intersection_crash = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS intersection_crash_count,                        
                        SUM(CASE WHEN c.motorcycle_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS motorcycle_flag_yes_count,  
                        SUM(CASE WHEN c.parked_vehicle_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS parked_vehicle_flag_yes_count,
                        SUM(CASE WHEN c.parking_lot_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS parking_lot_flag_yes_count,
                        SUM(CASE WHEN c.pedestrian_flag = 'Yes' THEN 1 ELSE 0 END)* 100000.0 / p.total AS pedestrian_flag_yes_count,
                        AVG(total_victims) as average_victims,
                        p.total AS population,
                        (COUNT(*) * 100000.0 / p.total) AS crashes_per_100k
                    FROM crashes AS c
                    JOIN population AS p
                    ON UPPER(c.municipality) = p.municipality
                    GROUP BY c.municipality, p.total""")
    
    conn.commit()
    conn.close()

def get_crashes_per_100k():
    """this method returns the crash data aggregated by population and standardized as a dataframe"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM crashes_per_100k", conn)
    conn.close()
    return df