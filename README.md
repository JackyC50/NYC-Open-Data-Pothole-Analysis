# NYC-Open-Data-Pothole-Analysis

Data Cleaning Report
Project Overview: This report details the steps taken to clean and improve the accuracy of NYC 311 pothole service call data. The dataset, sourced from NYC Open Data, contained missing values, inconsistencies, and mismatches in location-based information. The goal was to clean, validate, and standardize the dataset for better analysis and visualization.

Data Cleaning Steps & Fixes:

Data Extraction
  Script: extract_pothole_data.py
  Output Files: raw_nyc_311_data.csv, 
  Issues Found:
    34 missing closed dates
    3,103 blank community board entries
    95 unspecified community boards
      Borough mismatches:
        1,496 unspecified in QUEENS
        306 unspecified in MANHATTAN
        754 unspecified in BROOKLYN
        815 unspecified in BRONX
        356 records had boroughs listed as '0 Unspecified'
    39,731 missing latitude/longitude values (26.7% of dataset)

Adding Location Data
  Script: add_location_column.py
  Input: raw_nyc_311_data.csv
  Output: data_with_location_column.csv
  Fixes Applied:
    Added a ‘location’ column to help retrieve missing latitude/longitude values using Google’s Geocoding API.
    451 latitude/longitude values remained missing after this step.

Fetching Missing Coordinates
  Script: fetch_missing_coordinates.py
  Input: data_with_location_column.csv
  Output: data_with_coordinates.csv
  Fixes Applied:
    Used Google’s API to retrieve missing latitude/longitude values from the ‘location’ column.

Updating Community Board Data
  Script: update_community_board.py
  Input: data_with_coordinates.csv
  Output: data_with_gis_community_boards.csv
  Fixes Applied:
    Used GIS files to derive community board values based on latitude/longitude coordinates.
    652 community board values were still missing after this step.
  
Final Cleaning and Data Validation
  Script: final_cleaning_validation.ipynb
  Input: data_with_gis_community_boards.csv
  Output: final_cleaned_nyc_311_data.csv
  Fixes Applied:
    Identified and removed 652 records with missing GIS-based community board values.
    Eliminated null longitude, latitude, and closed date values.
    Filled in 2,592 missing community board values using GIS data.
    Found 8,508 mismatches between manually entered and GIS-derived community board values. Used GIS values as the correct ones.
    Removed 264 mismatched records where borough values conflicted due to location boundaries.

Final Adjustments & Review
  Discovered human errors in the original dataset, such as non-existent community boards (e.g., Queens 16, which does not exist).
  Decided to use community_board_GIS as the primary reference for borough and community board values.
  Standardized borough, community board, and location fields using GIS data.
  Fixed formatting issues in Tableau (e.g., removing ‘.0’ suffix from numbers).

Summary of Data Cleaning Results:
  Missing Data Resolved:
    Closed dates: All missing values fixed.
    Community boards: 2,592 missing values filled, 652 null records removed.
    Boroughs: Standardized using GIS-derived values.
    Latitude/Longitude: Reduced missing values from 39,731 to 451.
  Data Mismatches Corrected:
    8,508 mismatches between manual and GIS-derived community board values fixed.
    264 records omitted due to borough mismatches at district boundaries.
  Final Considerations:
  The community_board_GIS values were more accurate than manually entered community board data.
  Borough values were aligned to GIS-based community boards to avoid human errors.
  The cleaned dataset is now structured for better accuracy and analysis.
  This report summarizes the cleaning process applied to NYC 311 pothole data to ensure data quality for future analytics and decision-making.

Analysis in progress...

Link to NYC Open Data Pothole Analysis dashboard: 
https://public.tableau.com/app/profile/jacky.cai8025/vizzes
