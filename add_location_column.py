import pandas as pd

# Step 1: Load the dataset
file_path = 'raw_nyc_311_data.csv' # Update this with your file path
df = pd.read_csv(file_path)

# Step 2: Define a function to create the location column dynamically
def determine_location(row):
    if pd.notna(row["incident_address"]) and row["incident_address"].strip():
        # Use incident address if it exists
        return f"{row['incident_address']}, {row['borough']}, NY {row['incident_zip']}"
    elif pd.notna(row["intersection_street_1"]) and pd.notna(row["intersection_street_2"]):
        # Use intersection streets if address is not found
        return f"{row['intersection_street_1']} and {row['intersection_street_2']}, {row['borough']}, NY {row['incident_zip']}"
    elif pd.notna(row["cross_street_1"]):
        # Use cross_street_1 and borough if both are present
        return f"{row['cross_street_1']}, {row['borough']}, NY {row['incident_zip']}"
    else:
        # If none of the above, return an empty value
        return ""

# Step 3: Apply the function to create the location column
df["location"] = df.apply(determine_location, axis=1)

# Step 4: Save the updated DataFrame to a new CSV file
output_path = 'data_with_location_column.csv'  # Update this with your desired file path
df.to_csv(output_path, index=False)

print(f"Updated dataset saved to: {output_path}")
