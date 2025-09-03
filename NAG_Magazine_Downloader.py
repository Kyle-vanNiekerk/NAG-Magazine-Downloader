import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_pdfs_from_url(url):
    """
    Goes to the provided URL, finds links to PDF documents, and downloads them.
    The PDFs will be saved in a new directory named 'NAG_Magazines'.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the response was an error
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a directory to save the PDFs
    save_directory = "NAG_Magazines"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"Created directory: {save_directory}")

    # Find all anchor tags that contain an image
    links_with_images = soup.find_all('a')
    
    pdf_count = 0
    for link in links_with_images:
        href = link.get('href')
        if href and href.endswith('.pdf'):
            # Construct the full URL for the PDF
            pdf_url = urljoin(url, href)
            pdf_filename = os.path.basename(href)
            pdf_path = os.path.join(save_directory, pdf_filename)
            
            # Download the PDF
            try:
                print(f"Downloading {pdf_filename} from {pdf_url}...")
                pdf_response = requests.get(pdf_url, stream=True)
                pdf_response.raise_for_status()
                with open(pdf_path, 'wb') as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded {pdf_filename}")
                pdf_count += 1
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {pdf_filename}: {e}")

    if pdf_count > 0:
        print(f"\n{pdf_count} PDF(s) downloaded successfully.")
    else:
        print("\nNo PDF files found or downloaded.")

# The URL to scrape
url = "https://www.nag.co.za/nag-magazine-archives/"

# Run the function
download_pdfs_from_url(url)