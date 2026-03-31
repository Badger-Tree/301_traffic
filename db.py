import sqlite3
import csv

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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crashes (
        crash_breakdown_2 TEXT,
        date_of_loss_year INTEGER,
        animal_flag TEXT,
        crash_severity TEXT,
        cyclist_flag TEXT,
        day_of_week TEXT,
        derived_crash_config TEXT,
        heavy_veh_flag TEXT,
        intersection_crash TEXT,
        month_of_year INTEGER,
        motorcycle_flag TEXT,
        municipality_name_ifnull TEXT,
        parked_vehicle_flag TEXT,
        parking_lot_flag TEXT,
        pedestrian_flag TEXT,
        region TEXT,
        street_full_name_ifnull TEXT,
        time_category TEXT,
        municipality_name TEXT,
        road_location_description TEXT,
        street_full_name TEXT,
        metric_selector TEXT,
        total_crashes INTEGER,
        total_victims INTEGER,
        latitude REAL,
        longitude REAL,
        mid_block_crash TEXT,
        municipality_with_boundary TEXT,
        cross_street_full_name TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def import_crash_csv(file_path):
    """Import data from a CSV file into the crashes table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]  # strip BOM/whitespace

        for row in reader:
            total_crashes = int(row['Total Crashes']) if row['Total Crashes'] else None
            total_victims = int(row['Total Victims']) if row['Total Victims'] else None
            latitude = float(row['Latitude']) if row['Latitude'] else None
            longitude = float(row['Longitude']) if row['Longitude'] else None

            cursor.execute('''
                INSERT INTO crashes (
                    crash_breakdown_2, date_of_loss_year, animal_flag, crash_severity,
                    cyclist_flag, day_of_week, derived_crash_config, heavy_veh_flag,
                    intersection_crash, month_of_year, motorcycle_flag, municipality_name_ifnull,
                    parked_vehicle_flag, parking_lot_flag, pedestrian_flag, region,
                    street_full_name_ifnull, time_category, municipality_name,
                    road_location_description, street_full_name, metric_selector,
                    total_crashes, total_victims, latitude, longitude,
                    mid_block_crash, municipality_with_boundary, cross_street_full_name
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', [
                row['Crash Breakdown 2'], row['Date Of Loss Year'], row['Animal Flag'],
                row['Crash Severity'], row['Cyclist Flag'], row['Day Of Week'],
                row['Derived Crash Configuration'], row['Heavy Veh Flag'],
                row['Intersection Crash'], row['Month Of Year'], row['Motorcycle Flag'],
                row['Municipality Name (ifnull)'], row['Parked Vehicle Flag'], row['Parking Lot Flag'],
                row['Pedestrian Flag'], row['Region'], row['Street Full Name (ifnull)'],
                row['Time Category'], row['Municipality Name'], row['Road Location Description'],
                row['Street Full Name'], row['Metric Selector'], total_crashes,
                total_victims, latitude, longitude, row['Mid Block Crash'],
                row['Municipality With Boundary'], row['Cross Street Full Name']
            ])
    
    conn.commit()
    conn.close()

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
            municipality = row[1].strip().upper()  # uppercase
            total = int(row[5].replace(',', '').strip())  # remove commas
            cursor.execute('''
                INSERT INTO population (region, municipality, total)
                VALUES (?, ?, ?)
            ''', [region, municipality, total])
    
    conn.commit()
    conn.close()

# calculate municipal crashes
def create_crashes_per_100k():
    """calculate crashes per 100k in each municipality"""
    conn = get_connection()
    cursor = conn.cursor()
    # cursor.execute("DROP VIEW IF EXISTS crashes_per_100k")
    cursor.execute("DROP TABLE IF EXISTS crashes_per_100k")
    cursor.execute("""
                   CREATE TABLE crashes_per_100k AS
                    SELECT 
                        c.municipality_name,
                        COUNT(*) AS total_crashes,
                        (CASE WHEN c.animal_flag = 'Yes' THEN 1 ELSE 0 END) AS animal_flag_yes_count,
                        SUM(CASE WHEN c.cyclist_flag = 'Yes' THEN 1 ELSE 0 END) AS cyclist_flag_yes_count,
                        SUM(CASE WHEN c.heavy_veh_flag = 'Yes' THEN 1 ELSE 0 END) AS heavy_veh_flag_yes_count,
                        SUM(CASE WHEN c.intersection_crash = 'Yes' THEN 1 ELSE 0 END) AS intersection_crash_count,                        
                        SUM(CASE WHEN c.motorcycle_flag = 'Yes' THEN 1 ELSE 0 END) AS motorcycle_flag_yes_count,  
                        SUM(CASE WHEN c.parked_vehicle_flag = 'Yes' THEN 1 ELSE 0 END) AS parked_vehicle_flag_yes_count,
                        SUM(CASE WHEN c.parking_lot_flag = 'Yes' THEN 1 ELSE 0 END) AS parking_lot_flag_yes_count,
                        SUM(CASE WHEN c.pedestrian_flag = 'Yes' THEN 1 ELSE 0 END) AS pedestrian_flag_yes_count,
                        AVG(total_victims) as average_victims,
                        p.total AS population,
                        (COUNT(*) * 100000.0 / p.total) AS crashes_per_100k
                    FROM crashes AS c
                    JOIN population AS p
                    ON UPPER(c.municipality_name) = p.municipality
                    GROUP BY c.municipality_name, p.total""")
    
    conn.commit()
    conn.close()
#TODO: the crashes_per_100k table shows counts of crash flags, but not standardized to 100k