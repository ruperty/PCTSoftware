import json
import os

def read_dict_from_file(input_dir, file_name):
    """Read a dictionary from a JSON file in the specified directory."""
    file_path = os.path.join(input_dir, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_dict_to_files(data, output_dir):
    """Write the contents of each key in the dictionary to a separate JSON file in the specified directory, with a counter prefix."""
    os.makedirs(output_dir, exist_ok=True)
    for counter, (key, value) in enumerate(data.items(), start=1):
        file_name = f"{counter}_{key}.dat"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            json.dump(value, file, indent=4)

# Example usage
if __name__ == "__main__":
    input_directory = 'C:\\packages\\arc-prize-2024'
    output_directory = 'C:\\packages\\arc-prize-2024\\training'
    json_file_name = 'arc-agi_training_challenges.json'

    data_dict = read_dict_from_file(input_directory, json_file_name)
    write_dict_to_files(data_dict, output_directory)
