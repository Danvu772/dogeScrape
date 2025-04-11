import re
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def setup_driver():
    options = Options()
    options.add_argument('-headless')
    return Firefox(options=options)

def fetch_savings(url):
    driver = setup_driver()
    driver.get(url)
    table_types = ['contracts', 'grants', 'real_estate']
    for i in range(3):
        all_rows = []         
        table_header = '' 
        count = 1
        while True: 
            try:
                table_xpath = f'(//table)[{i + 1}]'
                skeleton_shine_xpath = f'{table_xpath}//div[contains(@class, "skeleton-shine")]'
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, skeleton_shine_xpath)))
                if not table_header:
                    header_xpath = f'{table_xpath}/thead'
                    header_element = driver.find_element(By.XPATH, header_xpath)
                    table_header = header_element.get_attribute("outerHTML")
                rows_xpath = f'{table_xpath}//tbody/tr'
                rows = driver.find_elements(By.XPATH, rows_xpath)
                for row in rows:
                    all_rows.append(row.get_attribute("outerHTML"))
                next_button_xpath = f'(//button[@aria-label="Next page"])[{i + 1}]'
                next_button = driver.find_element(By.XPATH, next_button_xpath)
                if next_button.get_attribute('disabled') is not None:
                    print(f"Next button is disabled for table {table_types[i]}. Ending pagination.")
                    break
                else:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                    next_button.click()
                    print(f"Accessing page {count} of table {table_types[i]}", end='\r')
                    count += 1
            except Exception as e:
                print(f"Unable to click next button. Finishing scrape for table {table_types[i]} on page {count}: {e}")
                break
        print(f"Finished scraping pages for table {table_types[i]}")
        table_html = f'<table>{table_header}<tbody>{"".join(all_rows)}</tbody></table>'
        table_filename = f'./scraped_html/{table_types[i]}.html'
        with open(table_filename, 'w', encoding='utf-8') as file:
            file.write(clean_html(table_html))
        print(f'Successfully saved: {table_filename}')
    driver.quit()

def fetch_payments(url):
    print('fetching payments html')
    driver = setup_driver()
    driver.get(url)
    view_all_xpath = f'//*[contains(text(), "View All")]'
    view_all_button = driver.find_element(By.XPATH, view_all_xpath)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, view_all_xpath)))
    view_all_button.click()
    print('clicked View All button')

    all_rows = []
    table_header = ''
    count = 1

    while True:
        try:
            table_xpath = f'(//table[1])'
            if not table_header:
                header_xpath = f'{table_xpath}/thead'
                header_element = driver.find_element(By.XPATH, header_xpath)
                table_header = header_element.get_attribute('outerHTML')
            rows_xpath = f'{table_xpath}//tbody/tr'
            rows = driver.find_elements(By.XPATH, rows_xpath)
            for row in rows:
                all_rows.append(row.get_attribute('outerHTML'))
            next_button_xpath = f'//button[text()="Next"]'
            next_button = driver.find_element(By.XPATH, next_button_xpath)
            if next_button.get_attribute('disabled') is not None:
                print(f'Next button is disabled. Ending pagination')
                break
            else: 
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                next_button.click()
                print(f'Accessing page {count}', end='\r')
                count += 1

        except Exception as e:
            print(f'Unable to scrape table: {e}')

    table_html = f'<table>{table_header}<tbody>{''.join(all_rows)}</tbody></table>'
    table_filename = f'./scraped_html/payments.html'
    with open(table_filename, 'w', encoding='utf-8') as file:
        file.write(clean_html(table_html))
    print(f'Successfully saved: {table_filename}')
    driver.quit()


def clean_html(html_content):
    html_content = re.sub(r'\n+', ' ', html_content)  # Replace multiple newline characters with a single space
    html_content = re.sub(r'\s+', ' ', html_content)  # Replace multiple spaces with a single space
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)  # Removes HTML comments
    html_content = re.sub(r'>\s+<', '><', html_content)  # Removes spaces between HTML tags
    return html_content
def main():
    #fetch_savings('https://doge.gov/savings')
    fetch_payments('https://doge.gov/payments')

if __name__ == main():
    main()
