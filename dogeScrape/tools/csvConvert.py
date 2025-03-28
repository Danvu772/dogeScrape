import os
import csv
import json

CSV_FOLDER = '../../api/static/csv_output'
JSON_FOLDER = '../../api/static/json_output'

def convert_csv_to_json(csv_filename):
    """Converts a single CSV file to JSON and saves it."""
    csv_path = os.path.join(CSV_FOLDER, csv_filename)
    json_filename = os.path.splitext(csv_filename)[0] + '.json'  # Replace .csv with .json
    json_path = os.path.join(JSON_FOLDER, json_filename)

    data = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        with open(json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Converted {csv_filename} → {json_filename}")
    except Exception as e:
        print(f"Error processing {csv_filename}: {e}")

def convert_all_csvs():
    if not os.path.exists(CSV_FOLDER):
        print(f"Directory {CSV_FOLDER} does not exist.")
        return

    csv_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    for csv_file in csv_files:
        convert_csv_to_json(csv_file)

def doinChecks():
    print(get_csv_files())
    print(get_json_files())

def get_csv_files():
    return [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]

def get_json_files():
    return [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]

if __name__ == '__main__':
    #convert_all_csvs()
    doinChecks()