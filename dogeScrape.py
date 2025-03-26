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
                # Wait for the shadow-div class to be present
                shadow_div_xpath = '//table/ancestor::div[2][contains(@class, "shadow-lg")]'
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, shadow_div_xpath)))

                # XPath for selecting the i-th table on the page
                table_xpath = f'(//table)[{i + 1}]'  # XPath to select the i-th table (1-based indexing)
                # Wait for the table to be located
                table_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
                html = table_element.get_attribute("outerHTML")
                
                # Append HTML to the corresponding table type
                table_content += html

                # Find the "Next" button by aria-label
                next_button_xpath = f'(//button[@aria-label="Next page"])[{i + 1}]'
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                
                # Check if the "Next" button is disabled
                if next_button.get_attribute('disabled') is not None:
                    print(f"Next button is disabled for table {table_types[i]}. Ending pagination.")
                    break  # Exit the loop if the button is disabled
                else:
                    # If the button is enabled, click it and wait for the page to load
                    next_button.click()
                    print(f"Accessing index {count} of table {table_types[i]}", end='\r')  # This will print the count
                    count += 1  # Increment count after each "Next" click

            except Exception as e:
                print(f"Error clicking next button for table {table_types[i]}: {e}")
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
