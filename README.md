# Group 4 Project 6 - EN.685.648

## Secondary Data Source - Property Values in Washington, D.C.
The secondary dataset consists of property taxes and assessed home values for Washington, D.C. 
The data were obtained from the D.C. Office of Tax and Revenue, which provides real property
information including  size, usage, property value, assessment, and neighborhood information. 
The usage information identifies whether the property is commericial or residential, and
includes additional information about the properties, such as whether the properties are single-
or multi-family homes, and the type of housing (row home, single family home, apartment, etc.). There
are more than 200,000 properties listed in the pubically available dataset. The property tax 
data were first released in October 2020, and are updated daily. 

For additional details on the D.C. property tax data from the Office of Tax and Revenue, please
visit [their website](https://otr.cfo.dc.gov/page/real-property-public-extract-records).

### Accessing the Secondary Dataset
The data from the D.C. Office of Tax and Revenue are included within this project repository, located
within `./datasets/secondary`. To download a .csv file of the original data:
- Navigate to the [Integrated Tax System Public Extract link](https://opendata.dc.gov/datasets/integrated-tax-system-public-extract/explore?showTable=true)
- Click the "Download" link to the left of the table
- Download the data as a .csv file 

### Fields Used In Analysis
The analysis described in the project report utilized the following fields from the Integrated
Tax System Public Extract Dataset:
- `PROPTYPE`: descriptive labels for property usage, including designation of various residential property types,
commerical properties, and vacant properties
- `NBHDNAME`: name of the neighborhood in which the property is located
- `ASSESSMENT`: tax-assessed value of the property

`NBHDNAME` values from the secondary dataset were mapped to corresponding neighborhood groupings used in the
primary dataset. 

# Running Project Notebooks
This project contains various Jupyter notebooks. The notebooks require Anaconda for Python 3.9. Setting up the 
[environment](https://gist.github.com/actsasgeek/954c73d28503eb67f01d12a12b1e1181)
created for EN.685.648 will ensure that all dependencies are installed. To run project notebooks, the script
`./datasets/datawarehouse.py` first needs to be run, where `.` is the root project directory. This will create the following:
- `./datasets/datawarehouse.sql`: .sql table structure containing tables and fields
- `./datasets/datawarehouse.db`: SQLite database file containing both primary and secondary datasets

Connections to the `datawarehouse.db` file are used in all of the Juptyer Notebooks.

## Project Structure
```bash
.
├── README.md
├── datasets
│   ├── datawarehouse.db
│   ├── datawarehouse.py
│   ├── datawarehouse.sql
│   ├── primary
│   │   ├── 2022_q2
│   │   │   ├── calendar.csv
│   │   │   ├── listings.csv
│   │   │   ├── neighbourhoods.csv
│   │   │   ├── neighbourhoods.geojson
│   │   │   ├── reviews-2.csv
│   │   │   └── reviews.csv
│   │   ├── 2022_q3
│   │   │   ├── calendar.csv
│   │   │   ├── listings.csv
│   │   │   ├── neighbourhoods.csv
│   │   │   ├── neighbourhoods.geojson
│   │   │   ├── reviews-2.csv
│   │   │   └── reviews.csv
│   │   ├── 2022_q4
│   │   │   ├── calendar.csv
│   │   │   ├── listings.csv
│   │   │   ├── neighbourhoods.csv
│   │   │   ├── neighbourhoods.geojson
│   │   │   ├── reviews-2.csv
│   │   │   └── reviews.csv
│   │   ├── 2023_q1
│   │   │   ├── calendar.csv
│   │   │   ├── listings.csv
│   │   │   ├── neighbourhoods.csv
│   │   │   ├── neighbourhoods.geojson
│   │   │   └── reviews-2.csv
│   │   └── airbnb_data_dict.xls
│   └── secondary
│       ├── DC_neighborhood_mapping.ipynb
│       ├── DC_tax_assessed.csv
│       ├── README.txt
│       ├── property_info.csv
│       ├── weather.csv
│       └── weather2.csv
└── eda
    └── eda.ipynb
```
