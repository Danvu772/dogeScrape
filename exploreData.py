import pandas as pd
import os

def main():
    output_dir = './csv_output/'

    csv_files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]

    for file in csv_files:
        full_url = output_dir + file
        df = pd.read_csv(full_url)
        print(f'length of {file}: {len(df)}')
        check_missing_data(full_url)

def check_missing_data(csv_file):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Check for 'missing data' in the entire DataFrame
    missing_data = df.map(lambda x: x == 'missing data')

    # Find rows and columns where 'missing data' is present
    if missing_data.any().any():
        print("Missing data found:")
        for column in missing_data.columns:
            if missing_data[column].any():
                print(f"Column '{column}' has missing data at the following rows:")
                missing_rows = missing_data[missing_data[column]].index.tolist()
                for row in missing_rows:
                    print(f" - Row {row}")
    else:
        print("No missing data found.")

main()
