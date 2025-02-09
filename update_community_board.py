import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Step 1: Load your dataset
data_path = 'data_with_coordinates.csv'  # Path to your dataset
df = pd.read_csv(data_path)

# Ensure the dataset has latitude and longitude columns
if 'latitude' not in df.columns or 'longitude' not in df.columns:
    raise ValueError("Dataset must have 'latitude' and 'longitude' columns.")

# Step 2: Load the NYC Community Districts shapefile
shapefile_path = '/Users/jackycai/Downloads/Community Districts/geo_export_de9d86ca-5ffd-41de-a5fe-a58f230d2a20.shp'
community_districts = gpd.read_file(shapefile_path)

# Debug: Check the column names in the shapefile
print("Shapefile Columns:", community_districts.columns)

# Step 3: Ensure the shapefile uses the correct CRS
community_districts = community_districts.to_crs("EPSG:4326")

# Step 4: Convert the dataset's latitude/longitude to geometric points
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Step 5: Perform a spatial join to match points with community districts
geo_df_with_community_board = gpd.sjoin(geo_df, community_districts, how="left", predicate="within")

# Debug: Check the result of the spatial join
print("Spatial Join Result Columns:")
print(geo_df_with_community_board.columns)

# Step 6: Create a new community_board column based on GIS values
if "boro_cd" in geo_df_with_community_board.columns:
    df['community_board_GIS'] = geo_df_with_community_board['boro_cd']  # Replace existing column with GIS values
else:
    raise KeyError("Column 'boro_cd' not found in the spatial join result. Check the shapefile column names.")

# Step 7: Save the updated dataset to a new CSV file
output_path = 'data_with_gis_community_boards'
df.to_csv(output_path, index=False)

print(f"Updated dataset saved to: {output_path}")
