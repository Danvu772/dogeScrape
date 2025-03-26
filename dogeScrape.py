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

    for i in range(3):
        table_content = ''
        count = 1
        while True:
            try:
                table_xpath = f'(//table)[{i + 1}]'
                table_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

                skeleton_shine_xpath = f'{table_xpath}//div[contains(@class, "skeleton-shine")]'
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, skeleton_shine_xpath)))

                html = table_element.get_attribute("outerHTML")
                table_content += html

                next_button_xpath = f'(//button[@aria-label="Next page"])[{i + 1}]'
                next_button = driver.find_element(By.XPATH, next_button_xpath)
                
                if next_button.get_attribute('disabled') is not None:
                    print(f"Next button is disabled for table {table_types[i]}. Ending pagination.")
                    break
                else:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                    next_button.click()
                    print(f"Accessing index {count} of table {table_types[i]}", end='\r')
                    count += 1

            except Exception as e:
                print(f"Unable to click next button. Finishing Scrape for table on index {count} for {table_types[i]}: {e}")
                break

        print(f"Accessing index {count} of table {table_types[i]}")

        table_filename = f'./scraped_html/{table_types[i]}.html'
        with open(table_filename, 'w', encoding='utf-8') as file:
            file.write(clean_html(table_content))
        print(f'Successfully saved: {table_filename}')

    driver.quit()

def clean_html(html_content):
    html_content = re.sub(r'\n+', ' ', html_content)
    html_content = re.sub(r'\s+', ' ', html_content)
    html_content = re.sub(r'title\s*=\s*"(.*?)"', lambda match: f'title="{match.group(1).strip()}"', html_content)
    return html_content

def main():
    fetch_html('https://doge.gov/savings')

if __name__ == main():
    main()
