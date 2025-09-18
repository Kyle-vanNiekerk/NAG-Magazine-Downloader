import os
import re
from urllib.parse import unquote

def rename_nag_pdfs(directory="NAG_Magazines"):
    """
    Renames PDF files in a specified directory to a cleaner format.
    
    The script handles:
    - URL-encoded characters like '%20' (space).
    - Standard monthly magazine files (e.g., '001NAG%20January%202015.pdf').
    - Special supplement files (e.g., '000NAG%20E3%20Supplement%202013.pdf').
    
    The new format for magazines is 'NAG yyyy-mm.pdf' (e.g., 'NAG 2015-01.pdf').
    The new format for supplements is 'NAG Supplement [Type] yyyy.pdf' (e.g., 'NAG Supplement E3 2013.pdf').
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    month_mapping = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 
        'May': '05', 'June': '06', 'July': '07', 'August': '08', 
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    # Regex to match monthly magazines and capture the month and year
    monthly_pattern = re.compile(r'NAG%20(\w+)%20(\d{4}).pdf$', re.IGNORECASE)
    
    # Regex to match special supplements and capture the supplement type and year
    supplement_pattern = re.compile(r'NAG%20(.*?)%20Supplement%20(\d{4}).pdf$', re.IGNORECASE)

    # Regex to handle other special cases
    special_pattern = re.compile(r'NAG%20(.+?)%20(\d{4}).pdf$', re.IGNORECASE)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            # Decode URL-encoded spaces (%20)
            decoded_filename = unquote(filename)
            original_path = os.path.join(directory, filename)
            new_filename = None

            # Check for monthly magazines
            match = monthly_pattern.search(filename)
            if match:
                month_name = match.group(1)
                year = match.group(2)
                # Normalize month name
                if month_name.upper() in [m.upper() for m in month_mapping]:
                    month_number = month_mapping[month_name.capitalize()]
                    new_filename = f"NAG {year}-{month_number}.pdf"
            else:
                # Check for supplements
                match = supplement_pattern.search(filename)
                if match:
                    supplement_type = match.group(1).replace('%20', ' ')
                    year = match.group(2)
                    new_filename = f"NAG Supplement {supplement_type} {year}.pdf"
                else:
                    # Check for other special cases like 'Xbox Insider'
                    match = special_pattern.search(filename)
                    if match:
                        special_name = match.group(1).replace('%20', ' ')
                        year = match.group(2)
                        new_filename = f"NAG {special_name} {year}.pdf"

            if new_filename:
                new_path = os.path.join(directory, new_filename)
                if not os.path.exists(new_path):
                    os.rename(original_path, new_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"Skipping '{filename}': '{new_filename}' already exists.")
            else:
                print(f"Could not parse and rename: {filename}")

# Run the script
rename_nag_pdfs()