import argparse
import pandas as pd
import os
from bs4 import BeautifulSoup
from html_cleaner import clean_html

def main():
    # Define valid table choices
    tableChoices = ['Contracts', 'Grants', 'RealEstate']

    parser = argparse.ArgumentParser(description="Scrape and process HTML tables for Contracts, Grants, or RealEstate.")
    parser.add_argument("table_format", choices=tableChoices + ["all"],
                        help="Specify the table format to process: 'Contracts', 'Grants', 'RealEstate', or 'all' to process everything.")
    args = parser.parse_args()

    # Process all table formats or a single one
    if args.table_format.lower() == "all":
        for choice in tableChoices:
            print(f"Processing: {choice}")
            dogeScrape(choice)
    else:
        dogeScrape(args.table_format)

def dogeScrape(table_format):
    # Map table formats to their respective scraping functions
    table_format_dict = {
        'Contracts': contractScrape,
        'Grants': grantScrape,
        'RealEstate': realEstateScrape
    }

    # Sanitize input
    if table_format not in table_format_dict:
        print(f"Error: Unsupported table format '{table_format}'.")
        return

    # Define file names
    input_file = f'DOGE{table_format}.html'
    output_file = f'DOGE{table_format}SavingsTable.csv'

    # Ensure directories are valid
    scraped_html_path = './scraped_html/'
    output_csv_path = './csv_output/'

    os.makedirs(scraped_html_path, exist_ok=True)  # Create if missing
    os.makedirs(output_csv_path, exist_ok=True)

    # Validate file paths
    input_file_path = os.path.join(scraped_html_path, input_file)
    cleaned_file = f'Cleaned_{input_file}'
    cleaned_file_path = os.path.join(scraped_html_path, cleaned_file)
    
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        return

    # Clean the HTML file
    print(f"Cleaning file: {input_file_path}")
    clean_html(input_file_path, cleaned_file_path)
    if not os.path.exists(cleaned_file_path):
        print(f"Error: Failed to clean file '{input_file_path}'.")
        return

    # Parse the cleaned HTML file
    try:
        with open(cleaned_file_path, 'r', encoding='utf-8') as doge:
            dogeSoup = BeautifulSoup(doge, 'html.parser')
    except Exception as e:
        print(f"Error reading cleaned file: {e}")
        return

    rows = dogeSoup.select('tr')

    # Call the appropriate scraping function
    print(f"Scraping data for: {table_format}")
    database = table_format_dict[table_format](rows)

    # Save data to a CSV file
    if database:
        df = pd.DataFrame(database)
        output_csv_full_path = os.path.join(output_csv_path, output_file)
        try:
            df.to_csv(output_csv_full_path, index=False)
            print(f"CSV file '{output_csv_full_path}' created successfully!")
            print(f"Number of entries: {len(df)}")
            print(df.head())
        except Exception as e:
            print(f"Error saving CSV file: {e}")
    else:
        print(f"No data found to save for {table_format}.")

    # Delete the cleaned file
    try:
        os.remove(cleaned_file_path)
        print(f"Deleted temporary cleaned file: {cleaned_file_path}")
    except Exception as e:
        print(f"Error deleting temporary file '{cleaned_file_path}': {e}")

# Scraping Functions
def realEstateScrape(rows):
    output = []
    for row in rows:
        try:
            columns = row.select('td')

            main_agency = columns[0].get('title', '') if len(columns) > 0 else ''
            location = columns[1].text.strip() if len(columns) > 1 else ''
            sq_ft = columns[2].get('title', '') if len(columns) > 2 else ''
            saved = float(columns[3].text.strip().replace('$', '').replace(',', '')) if len(columns) > 3 else 0.0

            output.append({
                'Main Agency': main_agency,
                'Location': location,
                'Sq_Ft': sq_ft,
                'Saved': saved
            })
        except Exception as e:
            print(f"Error processing row: {e}")
    return output

def grantScrape(rows):
    output = []
    for row in rows:
        try:
            columns = row.select('td')

            agency = columns[0].get('title', '') if len(columns) > 0 else ''
            uploaded_on = columns[1].text.strip() if len(columns) > 1 else ''
            description = columns[2].get('title', '') if len(columns) > 2 else ''
            saved = float(columns[3].text.strip().replace('$', '').replace(',', '')) if len(columns) > 3 else 0.0

            output.append({
                'Agency': agency,
                'Uploaded On': uploaded_on,
                'Description': description,
                'Saved': saved
            })
        except Exception as e:
            print(f"Error processing row: {e}")
    return output

def contractScrape(rows):
    output = []
    for row in rows:
        try:
            columns = row.select('td')

            agency = columns[0].get('title', '') if len(columns) > 0 else ''
            description = columns[1].get('title', '') if len(columns) > 1 else ''
            uploaded_on = columns[2].text.strip() if len(columns) > 2 else ''
            link = columns[3].find('a').get('href', '') if len(columns) > 3 and columns[3].find('a') else ''
            saved = float(columns[4].text.strip()[1:].replace(',', '')) if len(columns) > 4 else 0.0

            output.append({
                'Agency': agency,
                'Description': description,
                'Uploaded On': uploaded_on,
                'Link': link,
                'Saved': saved
            })
        except Exception as e:
            print(f"Error processing row: {e}")
    return output

# Run the main function
if __name__ == "__main__":
    main()
