import sys
import os
import json

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    return input_path, output_path

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        sys.exit(1)

def save_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to save JSON file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    input_path, output_path = parse_arguments()
    if input_path.endswith('.json'):
        data = load_json(input_path)
    if output_path.endswith('.json'):
        save_json(data, output_path)
        print(f"Data saved to {output_path}")
