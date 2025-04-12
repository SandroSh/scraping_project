import csv
import json
import os
from urllib.parse import urlparse, urljoin


def absolute_url(base_url, relative_link):
    """
    Convert a relative URL to an absolute URL, ensuring it always contains "/catalogue/"
    """
    # Get website root (e.g., "http://books.toscrape.com/")
    parsed_base = urlparse(base_url)
    root_url = f"{parsed_base.scheme}://{parsed_base.netloc}/"

    # Remove "../" navigation from relative link
    parts = relative_link.strip("/").split("/")
    cleaned_parts = [p for p in parts if p != ".."]
    clean_path = "/".join(cleaned_parts)

    # Enforce "/catalogue/" prefix
    if not clean_path.startswith("catalogue/"):
        enforced_path = f"catalogue/{clean_path}"
    else:
        enforced_path = clean_path

    # Combine with root URL
    return urljoin(root_url, enforced_path)

def extract_number(text):
    """Extract numeric value from text."""
    if not text:
        return 0

    import re
    numbers = re.findall(r'\d+\.?\d*', text)
    return float(numbers[0]) if numbers else 0


def save_books_to_csv(books, filename="books.csv", data_folder="data"):
    """
    Save a list of Book objects to a CSV file in the specified data folder

    Args:
        books (list): List of Book objects
        filename (str): Name of the CSV file (default: "books.csv")
        data_folder (str): Path to data folder (default: "data")
    """
    # Ensure data folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    filepath = os.path.join(data_folder, filename)

    fieldnames = ["title", "price", "rating", "availability", "category",
                  "url", "image_url", "description"]

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book.to_dict())