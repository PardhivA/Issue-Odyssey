import json
import os

def load_from_json(reponame, filename):
    #create folder if it doesn't exist
    # create_repo_folder(reponame)

    # Path to the JSON file
    file_path = os.path.join(reponame, filename)

    data = None

    # Return data from the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data

def append_to_json(data, file_path):
    # Read existing data from JSON file
    os.makedirs("testingTEJA", exist_ok=True)
    existing_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)

    # Update existing data with new data
    existing_data = list(existing_data)
    existing_data.append(data)

    # Write updated data back to JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)  # Optional: indent for pretty formatting

def write_to_json(data, reponame, filename):
  #create folder if it doesn't exist
    # create_repo_folder(reponame)

    # Path to the JSON file
    file_path = os.path.join(reponame, filename)

    # Write the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
# Example usage:
file_path = "testingTEJA/nigga.json"
new_data = {"va": "value"}  # Data to append

append_to_json(new_data, file_path)
append_to_json(new_data, file_path)
print(load_from_json("testingTEJA", "nigga.json"))
