# this version enables to scrape all documents & full htmls from any website.
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL certificate warnings (use with caution)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def create_folder(folder_path):
    """Creates a folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)

def get_unique_filename(url):
    """Generates a unique filename based on URL hash."""
    parsed_url = urlparse(url)
    file_name = hashlib.md5(url.encode()).hexdigest()
    return file_name + ".html"

def get_document_filename(url):
    """Extracts the filename from the URL for documents."""
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def save_content(content, folder_path, filename):
    """Saves content (text or binary) to a file."""
    with open(os.path.join(folder_path, filename), 'wb') as f:
        f.write(content)

def scrape_website(url, folder_path, visited=set(), depth=0, max_depth=3, common_tabs=None):
    """Recursively scrapes a website up to max_depth."""
    if depth > max_depth or url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        if common_tabs:
            for tab in common_tabs:
                for elem in soup.select(tab):
                    elem.decompose()

        # Save HTML content excluding header, footer, and common tabs
        html_folder = os.path.join(folder_path, 'htmls')
        create_folder(html_folder)
        filtered_content = soup.prettify('utf-8')
        save_content(filtered_content, html_folder, get_unique_filename(url))

        # Save documents
        doc_folder = os.path.join(folder_path, 'documents')
        create_folder(doc_folder)
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                if full_url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
                    save_content(requests.get(full_url, verify=False).content, doc_folder, get_document_filename(full_url))
                else:
                    scrape_website(full_url, folder_path, visited, depth + 1, max_depth, common_tabs)
                    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

if __name__ == '__main__':
    company_url = input("Enter the company website URL: ")
    parsed_url = urlparse(company_url)
    domain = parsed_url.netloc.split('.')[1] if 'www' in parsed_url.netloc else parsed_url.netloc.split('.')[0]
    output_folder = f'{domain}_scraped_data'
    common_tabs = ['#main-nav', '.footer', 'header', 'footer']

    create_folder(output_folder)
    scrape_website(company_url, output_folder, common_tabs=common_tabs)
