import csv
import json
import os
from urllib.parse import urljoin


def absolute_url(base_url:str,relative_url:str) -> str:
    return urljoin(base_url, relative_url)

def extract_number(text):
    try:
        start = text.find('(')
        if start == -1:
            return 0

        end = text.find(' ', start)

        if end == -1:
            return 0

        number_in_str = text[start + 1:end]

        return int(number_in_str)
    except (ValueError, IndexError) as e:
        print(f"Error extracting number: {e}")
        return -1


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