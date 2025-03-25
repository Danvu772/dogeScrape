import re

def clean_html(file_path, output_path):
    """
    Cleans an HTML file by removing unnecessary newlines, extra spaces,
    and special characters that might affect BeautifulSoup parsing.

    Parameters:
        file_path (str): Path to the input HTML file.
        output_path (str): Path to save the cleaned HTML file.
    """
    try:
        # Read the original HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Remove unnecessary newlines
        html_content = re.sub(r'\n+', ' ', html_content)

        # Normalize excessive spaces
        html_content = re.sub(r'\s+', ' ', html_content)

        # Clean `title` attributes by removing random spaces
        html_content = re.sub(r'title\s*=\s*"(.*?)"', lambda match: f'title="{match.group(1).strip()}"', html_content)

        # Save the cleaned HTML content to a new file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Cleaned HTML file saved as '{output_path}'")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

