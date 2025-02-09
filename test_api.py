import pandas as pd
import googlemaps
import time
import os

# Step 1: Check if there's a partially saved file
temp_path = 'file_with_coordinates_in_progress.csv'
if os.path.exists(temp_path):
    print(f"Resuming from the last saved progress: {temp_path}")
    df = pd.read_csv(temp_path)  # Load the partially updated dataset
else:
    file_path = 'updated_nyc_311_data.csv'  # Original dataset
    print(f"Starting from the original file: {file_path}")
    df = pd.read_csv(file_path)  # Load the original dataset

# Step 2: Initialize the Google Maps client
API_KEY = "YOUR API KEY"  # Replace with your actual API key
gmaps = googlemaps.Client(key=API_KEY)

# Step 3: Function to get latitude and longitude from the Google Maps API
def get_coordinates(location):
    try:
        # Send a geocoding request
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            return lat, lng
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {location}: {e}")
        return None, None

# Step 4: Initialize API call counter
api_calls = 0

# Step 5: Update missing latitude and longitude in the entire dataset
save_frequency = 1000  # Save progress every 1,000 rows

for index, row in df.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        # Get the location from the 'location' column
        location = row["location"]
        if pd.notna(location) and location.strip():
            print(f"Fetching coordinates for: {location}")
            lat, lng = get_coordinates(location)
            # Update the DataFrame with the new coordinates
            df.at[index, "latitude"] = lat
            df.at[index, "longitude"] = lng
            api_calls += 1  # Increment the counter

            # Throttle API requests to stay under rate limits
            time.sleep(0.03)  # Sleep for 30ms (33.3 requests/sec max)

            # Save progress every N rows
            if api_calls % save_frequency == 0:
                df.to_csv(temp_path, index=False)  # Overwrite the temporary file
                print(f"Progress saved after {api_calls} API calls.")

# Step 6: Save the final updated dataset to a new CSV file
output_path = 'file_with_coordinates.csv'
df.to_csv(output_path, index=False)

# Delete the temporary file after successful completion
if os.path.exists(temp_path):
    os.remove(temp_path)

print(f"Updated dataset saved to: {output_path}")
print(f"Total API calls made: {api_calls}")
