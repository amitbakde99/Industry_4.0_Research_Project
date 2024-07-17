from bs4 import BeautifulSoup
import os

def extract_main_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove header, footer, nav, script, style, and noscript elements
    for element in soup(['header', 'footer', 'nav', 'script', 'style', 'noscript']):
        element.decompose()

    # Find the main content area
    main_content = ""
    article = soup.find('article')
    if article:
        main_content = article.get_text(separator='\n', strip=True)
    else:
        main = soup.find('main')
        if main:
            main_content = main.get_text(separator='\n', strip=True)
        else:
            large_divs = soup.find_all('div')
            for div in large_divs:
                if len(div.get_text(strip=True)) > 200:  # Threshold length to identify large content blocks
                    main_content += div.get_text(separator='\n', strip=True) + '\n'
            if not main_content:  # Fallback if no large divs found
                body = soup.find('body')
                if body:
                    main_content = body.get_text(separator='\n', strip=True)

    return main_content

def save_to_text_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_html_files_in_directory(directory_path, output_file_path):
    combined_content = ""
    
    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.html'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Extract the main content
            main_content = extract_main_content(html_content)
            combined_content += main_content + "\n\n"

    # Save the combined content to a single text file
    save_to_text_file(combined_content, output_file_path)

# Directory containing HTML files
directory_path = r'C:\Users\amitb\Desktop\Coding\Industry 4.0 project\wipro_scraped_data\htmls'

# Output file path
output_file_path = r'C:\Users\amitb\Desktop\Coding\Industry 4.0 project\wipro_scraped_data\combined_html_content.txt'

# Process HTML files and combine content
process_html_files_in_directory(directory_path, output_file_path)

print(f'All content extracted and combined into {output_file_path}')
