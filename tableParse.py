import os
import pandas as pd
from bs4 import BeautifulSoup

def clean_dollar_amount(value):
    try:
        return float(value.replace('$', '').replace(',', '').strip())
    except ValueError:
        return value

def parse_tables(soup):
    tables = soup.find_all('table')
    if not tables:
        return None
    headers = [th.text.strip() for th in tables[0].find_all('th')]
    def extract_row_data(cells):
        return [
            cell.get('title') if cell.get('title') else
            next((element.get('title') for element in cell.find_all(True) if element.get('title')), None) or
            (cell.find('a')['href'] if cell.find('a') else
            (clean_dollar_amount(cell.text.strip()) if '$' in cell.text else
            (cell.text.strip() if cell.text.strip() else 'missing data')))
            if not cell.find('div', class_='skeleton-shine') 
            else 'missing data'
            for cell in cells
        ]
    all_rows = [
        extract_row_data(row.find_all('td')) + [''] * (len(headers) - len(row.find_all('td')))
        for table in tables
        for row in table.find_all('tr')[1:]
    ]
    return headers, all_rows

def save_to_csv(headers, rows, output_file):
    pd.DataFrame(rows, columns=headers).to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

def main():
    html_files = [
        #('./scraped_html/contracts.html', 'doge_contracts_savings.csv'),
        #('./scraped_html/grants.html', 'doge_grants_savings.csv'),
        #('./scraped_html/real_estate.html', 'doge_real_estate_savings.csv')
        ('./scraped_html/payments.html', 'doge_payments.csv')
    ]
    output_csv_folder = './web_scrape_csv_output/'
    os.makedirs(output_csv_folder, exist_ok=True)
    for html_path, csv_name in html_files:
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            result = parse_tables(soup)
            if result:
                headers, rows = result
                save_to_csv(headers, rows, os.path.join(output_csv_folder, csv_name))
            else:
                print(f"No tables found in {html_path}")

if __name__ == "__main__":
    main()
