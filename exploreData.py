import pandas as pd
import os


def main(output_dir1):
    
    output_dir = output_dir1

    csv_files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]

    totalSum = 0

    for file in csv_files:
        full_url = output_dir + file
        df = pd.read_csv(full_url)
        print(f'length of {file}: {len(df)}')

    for file in csv_files:
        full_url = output_dir + file
        fileSum = sum_csv(full_url)
        totalSum += fileSum
        print(f'sum of {file}: {format_as_dollar(fileSum)} ')

    
    print(f'total sum of all csvs is: {format_as_dollar(totalSum)}')
    

def sum_csv(csv_file):

    df = pd.read_csv(csv_file)
    csv_sum = df['value'].sum() 

    return csv_sum

def format_as_dollar(amount):
    return f"${amount:,.2f}"
    
main('./api_scrape_csv_output/')
main('./csv_output/')
    


