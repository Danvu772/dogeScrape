import os
import pandas as pd
from bs4 import BeautifulSoup

def clean_dollar_amount(value):
    """Converts dollar amounts to float, removing commas and '$' signs."""
    try:
        return float(value.replace('$', '').replace(',', '').strip())
    except ValueError:
        return value  # Return original value if conversion fails

def parse_tables(soup):
    """
    Parses multiple tables in an HTML file while:
    - Using headers only from the first table.
    - Collecting all rows (excluding header rows) from all tables.
    - Handling anchor (<a>) tags and dollar amounts.
    """
    tables = soup.find_all('table')

    if not tables:
        return None  # No tables found, return None

    # Extract headers from the first table
    headers = [th.text.strip() for th in tables[0].find_all('th')]

    all_rows = []
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header row in every table
        for row in rows:
            cells = row.find_all('td')
            row_data = []

            for cell in cells:
                cell_text = cell.text.strip()

                # Check for <a> tag in the cell and use the href attribute if present
                link = cell.find('a')
                if link and link.get('href'):
                    cell_text = link['href']  # Use the URL from the <a> tag

                # Check if the cell contains a dollar amount and convert to float
                if '$' in cell_text:
                    cell_text = clean_dollar_amount(cell_text)

                skeleton_div = cell.find('div', class_='skeleton-shine')
                if skeleton_div:
                    cell_text = 'missing data'
                    
                row_data.append(cell_text)

            # Ensure row has the correct number of columns (padding if necessary)
            if len(row_data) < len(headers):
                row_data.extend([''] * (len(headers) - len(row_data)))  # Pad missing cells

            all_rows.append(row_data)

    return headers, all_rows

def save_to_csv(headers, rows, output_file):
    """
    Saves extracted table data into a CSV file.
    """
    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

def main():
    html_files = [
        ('./scraped_html/contracts.html', 'doge_contracts_savings.csv'),
        ('./scraped_html/grants.html', 'doge_grants_savings.csv'),
        ('./scraped_html/real_estate.html', 'doge_real_estate_savings.csv')
    ]

    output_csv_folder = './csv_output/'
    os.makedirs(output_csv_folder, exist_ok=True)  # Ensure output folder exists

    for html_path, csv_name in html_files:
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            result = parse_tables(soup)
            if result:
                headers, rows = result
                csv_path = os.path.join(output_csv_folder, csv_name)
                save_to_csv(headers, rows, csv_path)
            else:
                print(f"No tables found in {html_path}")

if __name__ == "__main__":
    main()
