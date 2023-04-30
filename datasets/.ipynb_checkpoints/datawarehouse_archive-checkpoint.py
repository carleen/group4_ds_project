import xlrd
import os
import sqlite3
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
        out+=f'''    {field_vals[val]} {var_type},\n'''

    out+=f'''    {field_vals[len(field_vals)-1]} {var_type}
);\n\n'''
    
    # Automatically create the reviews table
    cur_sheet = variable_dict['calendar']
    field_vals = cur_sheet.col_values(0)[8:15]
    type_vals = cur_sheet.col_values(1)[8:15]

    out += f'''-- Table: calendar
DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar(
    id int PRIMARY KEY,
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
    
    pri
    text_file = open("datawarehouse.sql", "w")
    n = text_file.write(out)
    text_file.close()
    

def storeListings():
    pass

def storeListings_2():
    pass

def storeReviews():
    pass

def storeCalendar():
    pass

# List of year/quarter folder names
folder_list = ['2022_q2', '2022_q3', '2022_q4', '2023_q1']

# Name of .csv files to be examined
file_list = ['listings.csv', 'listings-2.csv', 'reviews-2.csv', 'calendar.csv']

# Connect to SQLITE database
database_path = './datawarehouse.db'
con = sqlite3.connect(database_path)
cur = con.cursor()

# Read in listings
i = 0
listings_df = pd.read_csv(f'./{folder_list[i]}/{file_list[0]}')


'''
**********************************************
                    BACKUP
**********************************************
'''

# Filter and save only departments
department_dict = {}

# Populate department_dict, checking to see if the sheet is a contractor
print('The following departments are being processed..')
for c in contractor_sheet_list:
    c_name = c.name
    if c_name.rfind('00)') != -1:
        department_dict[c_name] = c
        print(c_name)
        
# Find the unique contractors contained in all of the sheets.
contractor_list = []
for dept_name in department_dict:
    cur_sheet = department_dict[dept_name]
    
    # Get the column names, excluding the heading
    cur_sheet_dept = cur_sheet.col_values(0)[1:]
    
    # Only add the contractor to the "contractor_list" if it doesn't already exist there
    for contractor in cur_sheet_dept:
        contractor = contractor.replace('''\'''', '')
        contractor = contractor.replace('''\"''', '')
        if contractor not in contractor_list:
            contractor_list.append(contractor)
            
# Connect to SQLITE database, and update the "contractors" table
database_path = './contracts.db'
con = sqlite3.connect(database_path)
cur = con.cursor()

# Update the database to include each contractor
contractor_id = 1
for contractor in contractor_list:
    contractor_str =f'''{contractor_id}, \'{contractor}\''''
    command_str = f'''INSERT INTO contractors VALUES({contractor_str});'''
    cur.execute(command_str)
    con.commit()
    contractor_id+=1
    
# Check to see if it worked
cur.execute('SELECT * FROM contractors')
contractor_1 = cur.fetchone()
print(f'id: {contractor_1[0]}, global_vendor_name: {contractor_1[1]}')

'''
department: dept_name
actions: col 1
dollars: col 2
contractor_id (Foreign key)
'''
#query = f'''SELECT contractors.id FROM contractors WHERE global_vendor_name== {contractor_name} '''

actions_id = 1
for dept_name in department_dict:
    cur_sheet = department_dict[dept_name]
    
    # Get the column names, excluding the heading
    contractor_list = cur_sheet.col_values(0)[1:]
    actions_list = cur_sheet.col_values(1)[1:]
    dollars_list = cur_sheet.col_values(2)[1:]
    
    # Iterate through the lists
    for ind in range(0, len(contractor_list)):
        # Edit the format of the contractor string from the sheet to match contractor table
        contractor = contractor_list[ind]
        contractor = contractor.replace('''\'''', '')
        contractor = contractor.replace('''\"''', '')
        
        # Get contractor ID from the "contractors" table
        query = f'''SELECT contractors.id FROM contractors WHERE global_vendor_name== \'{contractor}\' '''
        cur.execute(query)
        contractor_id = cur.fetchone()[0]
        
        # Get actions and dollars values
        actions = actions_list[ind]
        dollars = dollars_list[ind]
        
        action_str = f'''{actions_id}, \'{dept_name}\', {actions}, {dollars}, {contractor_id}'''
        command_str = f'''INSERT INTO actions VALUES({action_str});'''
        cur.execute(command_str)
        con.commit()
        
        actions_id+=1

# Double check that our database was updated properly
query = '''SELECT * FROM actions'''
cur.execute(query)
r = cur.fetchall()

print('Veryifying actions table update, checking some table values...')
for s in r[0:2000:250]:
    print(s)
print('\n')

con.close()
