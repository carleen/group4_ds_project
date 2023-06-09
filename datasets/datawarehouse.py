import xlrd
import os
import sqlite3
import csv
import pandas as pd
import numpy as np

neighborhood_mapping = {'Woodley': 'Cleveland Park, Woodley Park, Massachusetts Avenue Heights, Woodland-Normanstone Terrace',
                        'Palisades': 
                        'Spring Valley, Palisades, Wesley Heights, Foxhall Crescent, Foxhall Village, Georgetown Reservoir', 
                       'Congress Heights': 
                        'Congress Heights, Bellevue, Washington Highlands',
                       'Georgetown':
                        'Georgetown, Burleith/Hillandale',
                       'Foggy Bottom':
                        'West End, Foggy Bottom, GWU',
                       'North Cleveland Park':
                        'North Cleveland Park, Forest Hills, Van Ness', 
                       'Deanwood': 
                        'Deanwood, Burrville, Grant Park, Lincoln Heights, Fairmont Heights',
                       'Capitol Hill':
                        'Capitol Hill, Lincoln Park',
                       'Brightwood': 
                        'Brightwood Park, Crestwood, Petworth', 
                       'Columbia Heights':
                        'Columbia Heights, Mt. Pleasant, Pleasant Plains, Park View', 
                       'Shepherd Park': 
                        'Colonial Village, Shepherd Park, North Portal Estates',
                       'Hillcrest':
                        'Fairfax Village, Naylor Gardens, Hillcrest, Summit Park', 
                       'Trinidad': 
                        'Ivy City, Arboretum, Trinidad, Carver Langston',
                        'Brentwood': 'Brookland, Brentwood, Langdon',
                        'Brookland': 'Brookland, Brentwood, Langdon',
                        'South Anacostia Park':'Historic Anacostia',
                        'Mount Pleasant': 'Columbia Heights, Mt. Pleasant, Pleasant Plains, Park View', 
                        'Anacostia': 'Historic Anacostia',
                        'Randle Heights':  'Twining, Fairlawn, Randle Highlands, Penn Branch, Fort Davis Park, Fort Dupont', 
                        'Riggs Park': 'Lamont Riggs, Queens Chapel, Fort Totten, Pleasant Hill', 
                        'Burleith': 'Georgetown, Burleith/Hillandale',
                        'Cleveland Park': 'Cleveland Park, Woodley Park, Massachusetts Avenue Heights, Woodland-Normanstone Terrace',
                        'Fort Dupont Park': 'Twining, Fairlawn, Randle Highlands, Penn Branch, Fort Davis Park, Fort Dupont', 
                        'Fort Lincoln': 'Woodridge, Fort Lincoln, Gateway',
                       'Wesley Heights': 'Spring Valley, Palisades, Wesley Heights, Foxhall Crescent, Foxhall Village, Georgetown Reservoir',
                        'Foxhall': 'Spring Valley, Palisades, Wesley Heights, Foxhall Crescent, Foxhall Village, Georgetown Reservoir', 
                        'Petworth': 'Brightwood Park, Crestwood, Petworth',
                        'Glover Park':'Cathedral Heights, McLean Gardens, Glover Park',
                        'Chevy Chase': 'Hawthorne, Barnaby Woods, Chevy Chase', 
                        'Forest Hills': 'North Cleveland Park, Forest Hills, Van Ness', 
                        'Kalorama':'Kalorama Heights, Adams Morgan, Lanier Heights',
                        'Eckington':'Edgewood, Bloomingdale, Truxton Circle, Eckington', 
                        'Colonial Village':'Colonial Village, Shepherd Park, North Portal Estates', 
                        'Garfield':'Woodland/Fort Stanton, Garfield Heights, Knox Hill',
                        'American University':'Friendship Heights, American University Park, Tenleytown', 
                        'Crestwood':'Brightwood Park, Crestwood, Petworth',
                        'Ledroit Park':'Howard University, Le Droit Park, Cardozo/Shaw',
                        'Marshall Heights':'Capitol View, Marshall Heights, Benning Heights',
                       'Woodridge': 'Woodridge, Fort Lincoln, Gateway', 
                     'Michigan Park':'North Michigan Park, Michigan Park, University Heights',
                    'Spring Valley':'Spring Valley, Palisades, Wesley Heights, Foxhall Crescent, Foxhall Village, Georgetown Reservoir',
                    'Takoma':'Takoma, Brightwood, Manor Park', 
                    'Woodley': 'Cleveland Park, Woodley Park, Massachusetts Avenue Heights, Woodland-Normanstone Terrace', 
                    'Barry Farms':'Sheridan, Barry Farm, Buena Vista',
                    'Massachusetts Avenue Heights':'Cleveland Park, Woodley Park, Massachusetts Avenue Heights, Woodland-Normanstone Terrace',
                    'Berkley': 'Hawthorne, Barnaby Woods, Chevy Chase', 
                    'Washington Navy Yard':'Near Southeast, Navy Yard',
                    'Glover - Archbold Parkway':'Cathedral Heights, McLean Gardens, Glover Park', 
                    'North Anacostia Park':'Historic Anacostia',
                    'National Arboretum':'Ivy City, Arboretum, Trinidad, Carver Langston',
                       'R. L. A. SW':  'Southwest Employment Area, Southwest/Waterfront, Fort McNair, Buzzard Point',
                       'Old City 1': 'Capitol Hill, Lincoln Park',
                       'Old City 2': 'Dupont Circle, Connecticut Avenue/K Street',
                       'Lily Ponds': 'Union Station, Stanton Park, Kingman Park',
                       'Central': 'Mayfair, Hillbrook, Mahaning Heights',
                       'Wakefield': 'Friendship Heights, American University Park, Tenleytown',
                       '16th Street Heights': 'Brightwood Park, Crestwood, Petworth',
                       'Kent': 'Spring Valley, Palisades, Wesley Heights, Foxhall Crescent, Foxhall Village, Georgetown Reservoir',
                       'Hawthorne': 'Brightwood Park, Crestwood, Petworth',
                        'R. L. A. NE': 'Capitol View, Marshall Heights, Benning Heights',
                       }

bath_mapping = {
    'private': {
        '1 bath': 1,
        '1.5 baths': 1.5,
        '1 private bath': 1,
        '2 baths': 2,
        '2.5 baths': 2.5,
        '3 baths': 3,
        '3.5 baths': 3.5,
        '4 baths': 4,
        '4.5 baths': 4.5,
        '5 baths': 5,
        '5.5 baths': 5.5,
        '6 baths': 6,
        '7 baths': 7,
        '7.5 baths': 7.5,
        '11 shared baths': 11,
        '15 baths': 15,
        '0 baths': 0
    },
    'shared': {
        '0 shared baths': 0,
        '1 shared bath': 1,
        '1.5 shared baths': 1.5,
        '2 shared baths': 2,
        '2.5 shared baths': 2.5,
        '3 shared baths': 3,
        '3.5 shared baths': 3.5,
        '4 shared baths': 4,
        '4.5 shared baths': 4.5,
        '5 shared baths': 5,
        '5.5 shared baths': 5.5,
        '6 shared baths': 6,
        '8 shared baths': 8,
        '11 shared baths': 11,
        'Half-bath': 0.5,
        'Shared half-bath': 0.5
    }
}

prop_type = {
 'Private room in townhouse': 'house',
'Entire townhouse': 'house',
'Entire rental unit': 'apt',
'Entire guest suite': 'house',
'Room in boutique hotel': 'hotel',
'Entire home': 'house',
'Entire condo': 'apt',
'Private room in bed and breakfast': 'house',
'Private room in home': 'house',
'Private room in rental unit': 'apt',
'Private room in condo': 'apt',
'Entire serviced apartment': 'apt',
'Shared room in hostel': 'hotel',
'Shared room in townhouse': 'house',
'Private room in resort': 'hotel',
'Room in hotel': 'hotel',
'Shared room in rental unit': 'apt',
'Entire guesthouse': 'house',
'Room in bed and breakfast': 'hotel',
'Private room in guest suite': 'house',
'Entire loft': 'apt',
'Entire vacation home': 'house',
'Private room in hostel': 'hotel',
'Room in hostel': 'hotel',
'Shared room in bed and breakfast': 'hotel',
'Shared room in home': 'house',
'Tower': 'unusual',
'Castle': 'unusual',
'Room in aparthotel': 'hotel',
'Private room in guesthouse': 'house',
'Entire place': 'house',
'Private room in loft': 'apt',
'Entire bungalow': 'unusual',
'Private room': 'house',
'Casa particular': 'unusual',
'Private room in villa': 'house',
'Floor': 'apt', 
'Room in serviced apartment': 'apt',
'Tiny home': 'unusual',
'Shared room in guesthouse': 'house',
'Entire cottage': 'unusual',
'Shared room in hotel': 'hotel',
'Camper/RV': 'unusual',
'Houseboat': 'unusual',
'Shared room in loft': 'apt',
'Private room in casa particular': 'unusual',
'Private room in bungalow': 'unusual',
'Private room in serviced apartment': 'apt',
'Tent': 'unusual',
'Campsite': 'unusual',
'Shared room in serviced apartment': 'apt',
'Entire villa': 'unusual',
'Boat': 'unusual'
}


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

    out += f'''-- Table: property_info
DROP TABLE IF EXISTS property_info;
CREATE TABLE property_info(
    PROPTYPE text,
    NBHDNAME text,
    ASSESSMENT float
);'''
    
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
    print('Writing primary dataset to datawarehouse.db...')
    listings_csv_list = []
    fnames = ['2023_q1', '2022_q4', '2022_q3', '2022_q2']
    for f in fnames:
        temp_listings = f'./primary/{f}/listings.csv'
        temp_reviews = f'./primary/{f}/reviews-2.csv'
        temp_calendar = f'./primary/{f}/calendar.csv'
        storeListings(temp_listings)
        storeReviews(temp_reviews)
        storeCalendar(temp_calendar)
    #weather_listing = f'./secondary/weather.csv'
    #storeWeather(weather_listing)

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

def storePropertyInfo(csv_path):
    print('Writing secondary dataset to datawarehouse.db...')
    database_path = './datawarehouse.db'
    con = sqlite3.connect(database_path)
    cur = con.cursor()


    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proptype = row[7]
            nbhdname=row[200]
            assessment = row[61]
            
            try:
                nbhdname = neighborhood_mapping[nbhdname]
                cur.execute('''INSERT INTO property_info (PROPTYPE, NBHDNAME, ASSESSMENT)
VALUES (?, ?, ?);''', (proptype, nbhdname, assessment))
            except KeyError:
                continue


    f.close()

    con.commit()
    con.close()
    
def createCleanedCSV():
    database_path = './datawarehouse.db'
    db_path = database_path
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = '''
        SELECT NBHDNAME, AVG(ASSESSMENT),
          CASE
            WHEN AVG(ASSESSMENT) >= 1000000 THEN 'high' 
            WHEN AVG(ASSESSMENT) >= 600000 THEN 'medium' 
            ELSE 'low' 
          END AS assessment_tier
        FROM property_info
        WHERE PROPTYPE LIKE '%Residential%'
        GROUP BY NBHDNAME
        ORDER BY AVG(ASSESSMENT) DESC;'''

    cur.execute(query)

    avg_assess = cur.fetchall()
    con.close()
    assess_df = pd.DataFrame(avg_assess, columns=['neighborhood', 'price', 'label'])
    nbhd_group = []
    avg_assessment = []
    label = []
    nbhd_dict={}
    for p in avg_assess:
        nbhd_dict[p[0]] = p[2]

    nbhd_dict['Shaw, Logan Circle'] = 'medium'
    nbhd_dict['Downtown, Chinatown, Penn Quarters, Mount Vernon Square, North Capitol Street'] = 'medium'
    nbhd_dict['River Terrace, Benning, Greenway, Dupont Park'] = 'medium'
    nbhd_dict['Eastland Gardens, Kenilworth'] = 'low'
    nbhd_dict['Douglas, Shipley Terrace'] = 'low'    
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    query = '''
        SELECT neighbourhood_cleansed, CAST(REPLACE(price, '$', '') AS FLOAT), 
        bathrooms_text,
        CAST(bedrooms AS INT),
        CAST(beds AS INT),
        CAST(accommodates AS INT),
        host_is_superhost,
        host_response_time,
        room_type,
        property_type,
        instant_bookable,
           CAST(REPLACE(host_response_rate, '%', '') AS FLOAT),
           CAST(REPLACE(host_acceptance_rate, '%', '') AS FLOAT),
            CAST(REPLACE(number_of_reviews, '%', '') AS INT),
            CAST(review_scores_rating AS FLOAT),
            CAST(reviews_per_month AS FLOAT)
        FROM listings;'''

    cur.execute(query)

    listings = cur.fetchall()
    con.close()
    
    listings_df = pd.DataFrame(listings, columns = ['neighborhood', 'price', 'bathrooms', 
                                                'bedrooms', 'beds', 'accommodates', 
                                                'host_is_superhost', 'host_response_time',
                                               'room_type', 'property_type', 'instant_bookable',
                                               'host_response_rate', 'host_acceptance_rate', 
                                               'number_of_reviews', 'review_scores_rating',
                                               'reviews_per_month'])
    # Create a new column "neighborhood_label" based on the values in the "neighborhood" column
    listings_df['neighborhood_label'] = listings_df['neighborhood'].map(nbhd_dict)
    
    # create mapping for shared/private and number of baths

    # create new column for shared/private
    listings_df['bathroom_type'] = listings_df['bathrooms'].apply(lambda x: 'private' if 'private' in x.lower() else 'shared')

    # create new column for number of baths
    listings_df['num_baths'] = listings_df['bathrooms'].apply(lambda x: bath_mapping[listings_df['bathroom_type'][0]].get(x, None))

    listings_df['bathroom_type'].fillna(listings_df['bathroom_type'].mode()[0], inplace=True)
    listings_df['num_baths'].fillna(listings_df['num_baths'].median(), inplace=True)
    listings_df = listings_df.drop('neighborhood', axis=1)
    listings_df['property_type'] = listings_df['property_type'].map(prop_type)
    # Fill NA variables for superhost, bedrooms, beds, and accommodates
    listings_df['bedrooms'].fillna(np.median(listings_df.bedrooms), inplace=True)

    listings_df['beds'].fillna(np.median(listings_df.beds), inplace=True)

    listings_df['host_is_superhost'].replace('', listings_df.host_is_superhost.mode()[0], inplace=True)

    listings_df['host_response_time'].fillna(listings_df.host_response_time.mode()[0], inplace=True)
    listings_df['host_response_time'].replace('N/A', listings_df.host_response_time.mode()[0], inplace=True)
    listings_df['host_response_time'].replace('', listings_df.host_response_time.mode()[0], inplace=True)

    listings_df['room_type'].replace('Hotel room', 'Private room', inplace=True)

    listings_df['host_response_rate'].replace('', np.median(listings_df.host_response_rate), inplace=True)

    listings_df['review_scores_rating'].replace('', np.mean(listings_df.review_scores_rating), inplace=True)

    listings_df = listings_df.drop('bathrooms', axis=1)
    listings_df.to_csv('./airbnb_selected_variables.csv')
    

if __name__ == "__main__":
    database_path = './datawarehouse.db'
    createSQLFile()
    createDatabaseFile()
    bulkStoreListings()
    storePropertyInfo('./secondary/property_info.csv')
    createCleanedCSV()
    print('Complete! datawarehouse.db file successfully created.')

