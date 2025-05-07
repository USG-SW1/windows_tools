import sys
import os
import csv

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def parser_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Read the first line as header
        if header:
            print("Header items:", header)
        else:
            print("The file is empty or has no header.")
        # Initialize a dictionary to count occurrences for each relevant header
        counts = {key: {} for key in ['firmware', 'daemon', 'major_version', 'sn', 'model']}
        
        # Iterate through the rows and count occurrences
        for row in reader:
            # Check 'firmware' content length, skip the record if not equal to 12
            if 'firmware' in header:
                firmware_index = header.index('firmware')
                if len(row[firmware_index]) != 12:
                    continue
            for key in counts:
                if key in header:
                    index = header.index(key)
                    value = row[index]
                    counts[key][value] = counts[key].get(value, 0) + 1

        # Print the results
        for key, value_counts in counts.items():
            print(f"\nCounts for '{key}':")
            for value, count in value_counts.items():
                if value in ['rte:2', 'rte:3', 'ch', 'cli']:
                    if value == 'rte:2':
                        value = 'fp-rte:2'
                    elif value == 'rte:3':
                        value = 'fp-rte:3'
                    elif value == 'ch':
                        value = 'connectivity-ch'
                    elif value == 'cli':
                        value = 'fp-cli'
                print(f"  {value}: {count}")

def main():
    if len(sys.argv) != 2:
        print("Usage: parser_core_dump.py <file.csv>")
        sys.exit(1)

    file_name = sys.argv[1]
    if not file_name.lower().endswith('.csv'):
        print("Error: The file must be a .csv file.")
        print("Usage: parser_core_dump.py <file.csv>")
        sys.exit(1)

    if not os.path.isfile(file_name):
        print(f"Error: File '{file_name}' does not exist.")
        sys.exit(1)

    print(f"Processing file: {file_name}")
    parser_csv(file_name)
    print("File processed successfully.")

if __name__ == "__main__":
    main()