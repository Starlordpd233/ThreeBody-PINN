import os
import re

# Define the folder path
folder_path = "<home>/Desktop/3_body_problem/simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard"

# Get all files in the folder
files = os.listdir(folder_path)

# Process each file
for file in files:
    # Check if it's a Brutus file with the expected pattern
    if file.startswith("brutus_hierarchical_") and file.endswith(".txt"):
        # Extract the number part using regex
        match = re.search(r'brutus_hierarchical_(\d{4})\.txt', file)
        if match:
            number = match.group(1)
            # Create the new filename with 'gold' in it
            new_filename = f"brutus_hierarchical_gold_{number}.txt"
            
            # Get full paths for rename operation
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_filename}")

print("Renaming completed for brutus_hierarchical_gold_standard folder!")