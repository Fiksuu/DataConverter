import sys
import json
import xml.etree.ElementTree as ET
import yaml

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

def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"Failed to load XML file: {e}")
        sys.exit(1)

def save_xml(data, file_path):
    try:
        root = dict_to_xml('root', data)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print(f"Failed to save XML file: {e}")
        sys.exit(1)

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        sys.exit(1)

def save_yaml(data, file_path):
    try:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file)
    except Exception as e:
        print(f"Failed to save YAML file: {e}")
        sys.exit(1)

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        if isinstance(val, dict):
            child.extend(dict_to_xml(key, val))
        else:
            child.text = str(val)
        elem.append(child)
    return elem

if __name__ == "__main__":
    input_path, output_path = parse_arguments()
    if input_path.endswith('.json'):
        data = load_json(input_path)
    elif input_path.endswith('.xml'):
        data = load_xml(input_path)
    elif input_path.endswith('.yaml') or input_path.endswith('.yml'):
        data = load_yaml(input_path)
    else:
        print("Unsupported input format")
        sys.exit(1)

    if output_path.endswith('.json'):
        save_json(data, output_path)
    elif output_path.endswith('.xml'):
        save_xml(data, output_path)
    elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
        save_yaml(data, output_path)
    else:
        print("Unsupported output format")
        sys.exit(1)

    print(f"Data converted and saved to {output_path}")
