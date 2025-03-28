import pandas as pd
import os

output_dir = './csv_output/'

def main():

    csv_files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]

    totalSum = 0

    for file in csv_files:
        full_url = output_dir + file
        df = pd.read_csv(full_url)
        print(f'length of {file}: {len(df)}')
        check_missing_data(full_url)

    for file in csv_files:
        full_url = output_dir + file
        fileSum = sum_csv(full_url)
        totalSum += fileSum
        print(f'sum of {file}: {format_as_dollar(fileSum)} ')

    
    print(f'total sum of all csvs is: {format_as_dollar(totalSum)}')
    

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
                    print(f" - Row {row+2}")
    else:
        print("No missing data found.")

def sum_csv(csv_file):
    total_sum = 0

    df = pd.read_csv(csv_file)
    csv_sum = df.iloc[:, -1].sum() 

    return csv_sum

def format_as_dollar(amount):
    return f"${amount:,.2f}"
    
main()


