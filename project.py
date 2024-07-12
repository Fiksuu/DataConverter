import sys
import json
import xml.etree.ElementTree as ET
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

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
        indent_xml(root)  # Dodajemy formatowanie
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

def indent_xml(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class DataConverterUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Converter')

        layout = QVBoxLayout()

        self.label = QLabel('Select input and output files:')
        layout.addWidget(self.label)

        self.inputButton = QPushButton('Select Input File')
        self.inputButton.clicked.connect(self.select_input_file)
        layout.addWidget(self.inputButton)

        self.outputButton = QPushButton('Select Output File')
        self.outputButton.clicked.connect(self.select_output_file)
        layout.addWidget(self.outputButton)

        self.convertButton = QPushButton('Convert')
        self.convertButton.clicked.connect(self.convert_files)
        layout.addWidget(self.convertButton)

        self.setLayout(layout)

        self.input_file = None
        self.output_file = None

    def select_input_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)", options=options)
        if file:
            self.input_file = file
            self.label.setText(f"Selected input file: {file}")

    def select_output_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)", options=options)
        if file:
            self.output_file = file
            self.label.setText(f"Selected output file: {file}")

    def convert_files(self):
        if not self.input_file or not self.output_file:
            QMessageBox.warning(self, "Error", "Please select both input and output files.")
            return

        try:
            if self.input_file.endswith('.json'):
                data = load_json(self.input_file)
            elif self.input_file.endswith('.xml'):
                data = load_xml(self.input_file)
            elif self.input_file.endswith('.yaml') or self.input_file.endswith('.yml'):
                data = load_yaml(self.input_file)
            else:
                QMessageBox.warning(self, "Error", "Unsupported input format")
                return

            if self.output_file.endswith('.json'):
                save_json(data, self.output_file)
            elif self.output_file.endswith('.xml'):
                save_xml(data, self.output_file)
            elif self.output_file.endswith('.yaml') or self.output_file.endswith('.yml'):
                save_yaml(data, self.output_file)
            else:
                QMessageBox.warning(self, "Error", "Unsupported output format")
                return

            QMessageBox.information(self, "Success", f"Data converted and saved to {self.output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert files: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DataConverterUI()
    ex.show()
    sys.exit(app.exec_())
