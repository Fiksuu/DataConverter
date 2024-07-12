import sys
import os

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    return input_path, output_path

if __name__ == "__main__":
    input_path, output_path = parse_arguments()
    print(f"Input: {input_path}, Output: {output_path}")
