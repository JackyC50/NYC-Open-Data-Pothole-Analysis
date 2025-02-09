import pandas as pd
import requests
import time
import os

# Define the API endpoint
url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

# Function to read the API token from a file
def read_api_token():
    token_file = 'api_token.txt'  # Store the token in this file
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()  # Read and strip any extra spaces/newlines
    else:
        print("API token file not found.")
        return None

# Read the API token from the file
api_token = read_api_token()
if not api_token:
    print("Unable to proceed without the API token.")
    exit(1)  # Exit the script if no token is found

# Parameters to filter 2024 data with specific resolution_descriptions
params = {
    "$where": (
        "created_date >= '2020-01-01T00:00:00' AND created_date < '2025-01-01T00:00:00' AND "
        "complaint_type = 'Street Condition' AND "
        "descriptor = 'Pothole' AND "
        "("
        "resolution_description = 'The Department of Transportation inspected this complaint and repaired the problem.' OR "
        "resolution_description = 'The Department of Transportation inspected this complaint and found that the problem was fixed.' OR "
        "resolution_description = 'The Department of Transportation inspected this complaint and found that the defect was not accessible. The repair will be rescheduled.' OR "
        "resolution_description = 'The Department of Transportation inspected this complaint and referred it to the Arterial Division for further action' OR "
        "resolution_description = 'The Department of Transportation inspected this complaint and will schedule the repair'"
        ")"
    ),
    "$limit": 25000,  # Fetch 25000 rows per request
    "$$app_token": api_token  # Include the token in the request
}

# Define the correct column names (manually set columns)
column_names = ['unique_key', 'created_date', 'closed_date', 'complaint_type', 'descriptor',
               'incident_zip', 'incident_address', 'street_name', 'cross_street_1', 'cross_street_2', 'intersection_street_1','intersection_street_2','address_type','city',
               'resolution_description','resolution_action_updated_date','community_board','borough',
               'latitude','longitude']

# Define the file paths
csv_file = "2024_nyc_311_data_test2.csv"
progress_file = "download_progressTest2.txt"

# Function to get the last saved offset (if any)
def get_last_offset():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return int(f.read().strip())  # Read the last offset
    return 0  # Start from the beginning if no progress file exists

# Function to save the offset to a file
def save_offset(offset):
    with open(progress_file, 'w') as f:
        f.write(str(offset))

offset = get_last_offset()

# Write headers manually to the file
headers = column_names
with open(csv_file, "w", newline='', encoding='utf-8') as f:
    f.write(",".join(headers) + "\n")  # Write the headers as a single line separated by commas

# Open the file again for appending data
with open(csv_file, "a", newline='', encoding='utf-8') as f:
    # Loop to fetch data in chunks
    while True:
        params["$offset"] = offset  # Set the current offset for pagination
        
        # Make the API request
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if not data:  # If no data is returned, break the loop
                print("No more data to fetch.")
                break

            # Convert the current chunk of data into a DataFrame
            df = pd.DataFrame(data)

            # Ensure the columns align with the predefined names
            df = df[column_names]

            # Append data to the CSV without writing headers again
            df.to_csv(f, header=False, index=False)

            # Increment the offset for the next chunk
            offset += len(data)
            save_offset(offset)  # Save the current offset for resumption
            print(f"Fetched {len(data)} records, total offset: {offset}")

            # Delay to avoid hitting rate limits
            time.sleep(2)  # Adjust as needed
        else:
            print(f"Request failed with status code: {response.status_code}")
            break

print("Data fetching complete.")
