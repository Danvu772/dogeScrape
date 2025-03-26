import pandas as pd
import os
from bs4 import BeautifulSoup

def parse_table(table):
    """
    Extracts data from a BeautifulSoup table element into a structured format.
    """
    extracted_data = []
    headers = []
    
    # Extract headers
    for th in table.find_all('th'):
        header_text = th.text.strip()  # Strip any surrounding whitespace from the header text
        headers.append(header_text)

    # Extract rows
    rows = table.find_all('tr')[1:]  # Skip header row
    
    table_data = {
        "headers": headers,
        "rows": []
    }
    
    # Process each row
    for row in rows:
        cells = row.find_all('td')
        row_data = {}

        for i in range(len(headers)):
            if i < len(cells):  
                cell = cells[i]
                cell_text = cell.text.strip()

                link = None
                if cell.find('a'):
                    link = cell.find('a').get('href', '') 
                    cell_text = cell.find('a').text.strip() 
                
                if '$' in cell_text:
                    try:
                        cell_text = cell_text.replace('$', '').replace(',', '')
                        cell_text = float(cell_text)
                    except ValueError:
                        pass  
                if link:
                    row_data[headers[i]] = link  
                else:
                    row_data[headers[i]] = cell_text  

            else:
                row_data[headers[i]] = ''  # Handle missing cells
            
        table_data["rows"].append(row_data)
    
    extracted_data.append(table_data)
    
    return extracted_data

def save_to_csv(data, output_path):
    """
    Saves the parsed data to CSV files.
    """
    tableMap = ['contracts', 'grants', 'real_estate']
    for i, table in enumerate(data):
        df = pd.DataFrame(table["rows"], columns=table["headers"])
        csv_file = os.path.join(output_path, f'doge_{tableMap[i]}_savings.csv')
        df.to_csv(csv_file, index=False)
        print(f"Saved: {csv_file}")

def main():
    output_csv = './csv_output/'

    html_files = [
        './scraped_html/contracts.html',
        './scraped_html/grants.html',
        './scraped_html/real_estate.html'
    ]

    all_data = []

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            html_soup = BeautifulSoup(html_content, 'html.parser')

            # Find all tables in the soup object
            tables = html_soup.find_all('table')

            # Parse each table
            for table in tables:
                scraped_data = parse_table(table)
                all_data.extend(scraped_data)  # Add parsed data to the list

    if all_data:
        save_to_csv(all_data, output_csv)
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
