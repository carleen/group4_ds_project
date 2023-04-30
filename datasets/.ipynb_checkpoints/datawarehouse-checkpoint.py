import xlrd
import os
import sqlite3
import csv
import pandas as pd

def createSQLFile():
    # Full path to xls, including filename
    xls_path = './primary/airbnb_data_dict.xls'
    airbnb_file = xlrd.open_workbook_xls(xls_path)
    airbnb_var_sheets = airbnb_file.sheets()

    variable_dict = {}
    print('Saved Data Dictonaries:')
    for s in airbnb_var_sheets:
        s_name = s.name
        var_stored = True

        if s_name.rfind('listings.csv detail v4') != -1:
            variable_dict['listings'] = s

        elif s_name.rfind('reviews.csv v1') != -1:
            variable_dict['reviews'] = s

        elif s_name.rfind('calendar.csv v2') != -1:
            variable_dict['calendar'] = s
        
        elif s_name.rfind('weather.csv v1') != -1:
            variable_dict['weather'] = s

        else:
            var_stored = False

        if var_stored:
            print(f'\t{s_name}')
            
    # Automatically create the listings table
    cur_sheet = variable_dict['listings']
    field_vals = cur_sheet.col_values(0)[8:82]
    type_vals = cur_sheet.col_values(1)[8:82]

    out = f'''-- Table: listings
DROP TABLE IF EXISTS listings;
CREATE TABLE listings(
    id int PRIMARY KEY,\n'''

    for val in range (1, len(field_vals)-1):
        var_type = type_vals[val]
        if var_type == 'boolean [t=true; f=false]':
            var_type = 'boolean'
        if var_type == '':
            var_type = 'blob'
        out+=f'''    {field_vals[val]} {var_type},\n'''

    out+=f'''    {field_vals[len(field_vals)-1]} {var_type}
);\n\n'''
    
    # Automatically create the reviews table
    cur_sheet = variable_dict['reviews']
    field_vals = cur_sheet.col_values(0)[8:14]
    type_vals = cur_sheet.col_values(1)[8:14]

    out += f'''-- Table: reviews
DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews(
    id int PRIMARY KEY,
    listing_id int,\n'''

    for val in range (1, len(field_vals)-1):
        var_type = type_vals[val]
        if var_type == 'boolean [t=true; f=false]':
            var_type = 'boolean'
        if var_type == '':
            var_type = 'blob'
        if field_vals[val]!='id':
            out+=f'''    {field_vals[val]} {var_type},\n'''

    out+=f'''    {field_vals[len(field_vals)-1]} {var_type}
);\n\n'''
    
    # Automatically create the calendar table
    cur_sheet = variable_dict['calendar']
    field_vals = cur_sheet.col_values(0)[8:15]
    type_vals = cur_sheet.col_values(1)[8:15]

    out += f'''-- Table: calendar
DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar(
    listing_id int,\n'''

    for val in range (1, len(field_vals)-1):
        var_type = type_vals[val]
        if var_type == 'boolean [t=true; f=false]':
            var_type = 'boolean'
        if var_type == '':
            var_type = 'blob'
        out+=f'''    {field_vals[val]} {var_type},\n'''
    out+=f'''    {field_vals[len(field_vals)-1]} {var_type}
);\n\n'''

    # Automatically create the weather table

    cur_sheet = variable_dict['weather']
    field_vals = cur_sheet.col_values(0)[8:41]
    type_vals = cur_sheet.col_values(1)[8:41]

    out += f'''-- Table: weather
DROP TABLE IF EXISTS weather;
CREATE TABLE weather(
    id int PRIMARY KEY,
    weatherdate datetime,\n'''
    for val in range (2, len(field_vals)-1):
        var_type = type_vals[val]
        if var_type == 'boolean [t=true; f=false]':
            var_type = 'boolean'
        if var_type == '':
            var_type = 'blob'
        out+=f'''    {field_vals[val]} {var_type},\n'''
    out+=f'''    {field_vals[len(field_vals)-1]} {var_type}
);\n\n'''

    
    print('Writing datawarehouse.sql file...')
    text_file = open("datawarehouse.sql", "w")
    n = text_file.write(out)
    text_file.close()


def createDatabaseFile():
    con = sqlite3.connect('datawarehouse.db')
    with open('datawarehouse.sql', 'r') as f:
        sql_script = f.read()
        con.executescript(sql_script)
    con.close()
    
def bulkStoreListings():
    listings_csv_list = []
    fnames = ['2023_q1', '2022_q4', '2022_q3', '2022_q2']
    for f in fnames:
        temp_listings = f'./primary/{f}/listings.csv'
        temp_reviews = f'./primary/{f}/reviews-2.csv'
        temp_calendar = f'./primary/{f}/calendar.csv'
        storeListings(temp_listings)
        storeReviews(temp_reviews)
        storeCalendar(temp_calendar)
    weather_listing = f'./secondary/weather.csv'
    storeWeather(weather_listing)

def storeListings(csv_path):
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    
    
    query = 'INSERT INTO listings VALUES (?, ?, ..., ?)'
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            listing_values = row
            num_vals = len(listing_values)
            if num_vals == 75:
                del listing_values[4]
                num_vals = 74
                
            query_str = '?, '* (num_vals-1) + '?'
            query = f'''INSERT INTO listings VALUES ({query_str})'''
            try:
                cur.execute(query, listing_values)
            except sqlite3.IntegrityError:
                continue
    
    f.close()
    con.commit()
    con.close()

def storeWeather(csv_path):
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()

    query = 'INSERT INTO weather VALUES (?, ?, ..., ?)'
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            listing_values = row
            num_vals = len(listing_values)
            query_str = '?, '* (num_vals-1) + '?'
            query = f'''INSERT INTO weather VALUES ({query_str})'''
            try:
                cur.execute(query, listing_values)
            except sqlite3.IntegrityError:
                continue
    f.close()
    con.commit()
    con.close()

def storeReviews(csv_path):
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()

    query = 'INSERT INTO reveiws VALUES (?, ?, ..., ?)'
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            listing_values = row
            num_vals = len(listing_values)
            query_str = '?, '* (num_vals-1) + '?'
            query = f'''INSERT INTO reviews VALUES ({query_str})'''
            try:
                cur.execute(query, listing_values)
            except sqlite3.IntegrityError:
                continue
    f.close()
    con.commit()
    con.close()

def storeCalendar(csv_path):
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    
    print(csv_path)

    query = 'INSERT INTO calendar VALUES (?, ?, ..., ?)'
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            listing_values = row
            num_vals = len(listing_values)
            query_str = '?, '* (num_vals-1) + '?'
            query = f'''INSERT INTO calendar VALUES ({query_str})'''
            cur.execute(query, listing_values)
            '''
            try:
                cur.execute(query, listing_values)
            except sqlite3.IntegrityError:
                continue
            '''
    f.close()
    con.commit()
    con.close()

def joinWeatherCalendar():
    # Join the weather and calendar tables
    print('Creating joined weather/calendar table...')
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    
    query = '''DROP TABLE if EXISTS calendar_weather;'''
    cur.execute(query)
    con.commit()

    query =f'''CREATE TABLE calendar_weather AS
SELECT *
FROM calendar
JOIN weather
ON DATE(weather.weatherdate) = DATE(calendar.date)
WHERE calendar.date >= '2022-01-01' AND calendar.date < '2022-02-01';'''
    cur.execute(query)
    con.commit()

    con.close()

if __name__ == "__main__":
    createSQLFile()
    createDatabaseFile()
    bulkStoreListings()
    #joinWeatherCalendar()

