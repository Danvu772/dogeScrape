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

def fetch_html(url):
    driver = setup_driver()
    driver.get(url)
    table_types = ['contracts', 'grants', 'real_estate']

    # Loop through each table and fetch its HTML
    for i in range(3):  # Adjust this if more tables are to be scraped
        table_content = ''
        count = 0  # Initialize the count outside the loop to track number of pages processed
        while True:  # Loop until the next button is disabled
            try:

                table_xpath = f'(//table)[{i + 1}]'  # XPath to select the i-th table (1-based indexing)
                table_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

                skeleton_shine_xpath = f'{table_xpath}//div[contains(@class, "skeleton-shine")]'
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, skeleton_shine_xpath)))

                html = table_element.get_attribute("outerHTML")
                table_content += html

                next_button_xpath = f'(//button[@aria-label="Next page"])[{i + 1}]'
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                
                if next_button.get_attribute('disabled') is not None:
                    print(f"Next button is disabled for table {table_types[i]}. Ending pagination.")
                    break  # Exit the loop if the button is disabled
                else:
                    next_button.click()
                    print(f"Accessing index {count} of table {table_types[i]}", end='\r')  # This will print the count
                    count += 1  # Increment count after each "Next" click

            except Exception as e:
                print(f"Unable to click next button. Finishing Scrape for table on index {count} for {table_types[i]}: {e}")
                break  # Exit the loop on error

        table_filename = f'./scraped_html/{table_types[i]}.html'  # Create filename dynamically
        with open(table_filename, 'w', encoding='utf-8') as file:
            file.write(clean_html(table_content))  # Ensure the content is cleaned
        print(f'Successfully saved: {table_filename}')

    driver.quit()

def clean_html(html_content):

    # Remove unnecessary newlines
    html_content = re.sub(r'\n+', ' ', html_content)

    # Normalize excessive spaces
    html_content = re.sub(r'\s+', ' ', html_content)

    # Clean `title` attributes by removing random spaces
    html_content = re.sub(r'title\s*=\s*"(.*?)"', lambda match: f'title="{match.group(1).strip()}"', html_content)

    # Save the cleaned HTML content to a new file
    return html_content


def main():
    fetch_html('https://doge.gov/savings')
if __name__ == main():
    main()