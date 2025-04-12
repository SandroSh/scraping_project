import json
import csv
import os
from typing import List, Dict, Any, Union, Optional
from src.book_scraper.models.book import Book
from src.book_scraper.models.category import Category
from src.requests_module.requests_manager import get_request
from bs4 import BeautifulSoup, Tag
from src.book_scraper.parser import parse_html, extract_product_details, get_next_page_url

class Processing:
    """
    Class for processing and storing scraped book and category data to files.
    Provides methods to save data in CSV and JSON formats with category support.
    """

    # Class variable to store all available categories
    categories_map = {}

    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        """Ensure the output directory exists, create if it doesn't."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def save_json(data: Union[List, Dict], filename: str, directory: str = "data") -> str:
        """
        Save data to a JSON file.

        Args:
            data: Data to save (list of dictionaries or dictionary)
            filename: Name of the file without extension
            directory: Directory to save the file in

        Returns:
            Path to the saved file
        """
        Processing.ensure_directory_exists(directory)
        full_path = os.path.join(directory, f"{filename}.json")

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {full_path}")
            return full_path
        except Exception as e:
            print(f"Error saving JSON data to {full_path}: {e}")
            return ""

    @staticmethod
    def save_csv(data: List[Dict], filename: str, directory: str = "data") -> str:
        """
        Save data to a CSV file.

        Args:
            data: List of dictionaries with the same keys
            filename: Name of the file without extension
            directory: Directory to save the file in

        Returns:
            Path to the saved file
        """
        if not data:
            print(f"No data to save to CSV file {filename}.csv")
            return ""

        Processing.ensure_directory_exists(directory)
        full_path = os.path.join(directory, f"{filename}.csv")

        try:
            # Get fieldnames from the first item
            fieldnames = list(data[0].keys())

            with open(full_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"Data successfully saved to {full_path}")
            return full_path
        except Exception as e:
            print(f"Error saving CSV data to {full_path}: {e}")
            return ""

    @classmethod
    def save_books(cls, books: List[Book], directory: str = "data", formats: List[str] = ["json", "csv"]) -> Dict[
        str, str]:
        """
        Save a list of books to files in specified formats.

        Args:
            books: List of Book objects
            directory: Directory to save the files in
            formats: List of formats to save the data in ("json", "csv")

        Returns:
            Dictionary with the paths to the saved files
        """
        if not books:
            print("No books to save")
            return {}

        book_dicts = [book.to_dict() for book in books]
        result_paths = {}

        if "json" in formats:
            json_path = cls.save_json(book_dicts, "books", directory)
            if json_path:
                result_paths["json"] = json_path

        if "csv" in formats:
            csv_path = cls.save_csv(book_dicts, "books", directory)
            if csv_path:
                result_paths["csv"] = csv_path

        return result_paths

    @classmethod
    def save_categories(cls, categories: List[Category], directory: str = "data",
                        formats: List[str] = ["json", "csv"], include_books: bool = True) -> Dict[str, str]:
        """
        Save a list of categories to files in specified formats.

        Args:
            categories: List of Category objects
            directory: Directory to save the files in
            formats: List of formats to save the data in ("json", "csv")
            include_books: Whether to include books in the category data

        Returns:
            Dictionary with the paths to the saved files
        """
        if not categories:
            print("No categories to save")
            return {}

        category_dicts = []
        for category in categories:
            cat_dict = category.to_dict()

            # If not including books, remove them from the dictionary
            if not include_books:
                cat_dict.pop("books", None)

            category_dicts.append(cat_dict)

        result_paths = {}

        if "json" in formats:
            json_path = cls.save_json(category_dicts, "categories", directory)
            if json_path:
                result_paths["json"] = json_path

        if "csv" in formats:
            # For CSV, we need to flatten the data if include_books is True
            if include_books:
                # Creating a separate books CSV with category information
                all_books = []
                for category in categories:
                    for book in category.books:
                        book_dict = book.to_dict()
                        book_dict["category_name"] = category.name
                        all_books.append(book_dict)

                if all_books:
                    books_csv_path = cls.save_csv(all_books, "category_books", directory)
                    if books_csv_path:
                        result_paths["csv_books"] = books_csv_path

            # Save the category data without books to CSV
            simplified_categories = []
            for cat_dict in category_dicts:
                simple_cat = {k: v for k, v in cat_dict.items() if k != "books"}
                simplified_categories.append(simple_cat)

            csv_path = cls.save_csv(simplified_categories, "categories", directory)
            if csv_path:
                result_paths["csv"] = csv_path

        return result_paths

    @classmethod
    def save_all_data(cls, books: List[Book] = None, categories: List[Category] = None,
                      directory: str = "data", formats: List[str] = ["json", "csv"]) -> Dict[str, Dict[str, str]]:
        """
        Save both books and categories data to files in specified formats.

        Args:
            books: List of Book objects
            categories: List of Category objects
            directory: Directory to save the files in
            formats: List of formats to save the data in ("json", "csv")

        Returns:
            Dictionary with paths to all saved files
        """
        result = {}

        if books:
            result["books"] = cls.save_books(books, directory, formats)

        if categories:
            result["categories"] = cls.save_categories(categories, directory, formats)

        return result

    @classmethod
    def fetch_all_categories(cls, base_url: str = "http://books.toscrape.com/") -> Dict[str, Dict]:
        """
        Fetch all available categories from the website and store them in the class variable.

        Args:
            base_url: Base URL of the website

        Returns:
            Dictionary mapping category names to their details
        """
        try:
            # Import parser functions from your module
            from src.book_scraper.parser import parse_html

            response = get_request(base_url)
            if not response or not hasattr(response, 'text'):
                print(f"Failed to fetch categories from {base_url}")
                return {}

            soup = parse_html(response.text)
            if not soup:
                return {}

            # Find the category navigation section
            side_categories = soup.select('.side_categories .nav-list > li > ul > li > a')

            categories_map = {}

            for category_link in side_categories:
                category_name = category_link.get_text(strip=True)
                category_url = category_link.get('href', '')

                # Build the full URL for the category
                if category_url:
                    category_url = base_url + category_url if not category_url.startswith('http') else category_url

                # Extract category ID from URL if possible
                category_id = None
                if category_url and '/' in category_url:
                    parts = category_url.rstrip('/').split('/')
                    for i, part in enumerate(parts):
                        if part == "category" and i + 2 < len(parts):
                            # Format is typically /category/books/category_id/
                            category_id = parts[i + 2].split('_')[1] if '_' in parts[i + 2] else None
                            break

                categories_map[category_name] = {
                    'name': category_name,
                    'url': category_url,
                    'id': category_id,
                    'book_count': 0
                }

            # Store in class variable for future use
            cls.categories_map = categories_map

            print(f"Fetched {len(categories_map)} categories from {base_url}")
            return categories_map

        except Exception as e:
            print(f"Error fetching categories: {e}")
            return {}

    @classmethod
    def get_category_by_name(cls, category_name: str) -> Optional[Dict]:
        """
        Get category details by name.

        Args:
            category_name: Name of the category

        Returns:
            Category details dictionary or None if not found
        """
        # If categories haven't been fetched yet, return None
        if not cls.categories_map:
            print("Categories have not been fetched yet. Call fetch_all_categories() first.")
            return None

        # Case-insensitive lookup
        for name, details in cls.categories_map.items():
            if name.lower() == category_name.lower():
                return details

        print(f"Category '{category_name}' not found. Available categories: {', '.join(cls.categories_map.keys())}")
        return None

    @classmethod
    def scrape_and_save(cls, base_url: str = "http://books.toscrape.com/",
                        category_name: str = None,
                        max_pages: int = 5,
                        directory: str = "data",
                        formats: List[str] = ["json", "csv"]) -> Dict[str, Dict[str, str]]:
        """
        Scrape books from the given URL for a specified number of pages and save the data.
        Can scrape by category if category_name is provided.

        Args:
            base_url: Base URL of the website to scrape
            category_name: Optional category name to scrape books from a specific category
            max_pages: Maximum number of pages to scrape
            directory: Directory to save the files in
            formats: List of formats to save the data in ("json", "csv")

        Returns:
            Dictionary with paths to all saved files
        """
        from bs4 import BeautifulSoup

        # Import here to avoid circular imports

        # If categories haven't been fetched yet, fetch them
        if not cls.categories_map:
            cls.fetch_all_categories(base_url)

        # If category_name is provided, use its URL instead of base_url
        if category_name:
            category_details = cls.get_category_by_name(category_name)
            if category_details:
                start_url = category_details['url']
                print(f"Scraping category: {category_name} from URL: {start_url}")
            else:
                print(f"Category '{category_name}' not found. Using base URL.")
                start_url = base_url
        else:
            start_url = base_url

        all_products = []
        next_page = start_url
        page_count = 0

        while next_page and page_count < max_pages:
            print(f"Fetching page {page_count + 1} of {max_pages}: {next_page}")

            try:
                response = get_request(next_page)
                if not response or not hasattr(response, 'text'):
                    print(f"Failed to fetch {next_page}")
                    break

                soup = parse_html(response.text)
                if not soup:
                    break

                page_products = extract_product_details(soup, base_url)
                all_products.extend(page_products)

                page_count += 1
                if page_count >= max_pages:
                    break

                next_page = get_next_page_url(soup, next_page)

            except Exception as e:
                print(f"Error during scraping: {e}")
                break

        # Convert products to Book objects
        books = []
        categories_dict = {}  # To track categories

        for product in all_products:
            try:
                # Extract price value (remove currency symbol)
                price_str = product.get('price', "0")
                if isinstance(price_str, str):
                    price_str = price_str.replace('£', '').strip()

                rating = product.get("rating", 0)

                # Determine the category name
                if category_name:
                    book_category = category_name
                else:
                    # Try to extract category from product URL or defaulting to "General"
                    book_url = product.get('link', '')
                    book_category = "General Books"

                    # Extract category from URL if possible
                    for cat_name, cat_details in cls.categories_map.items():
                        if cat_details['url'] and cat_details['url'] in book_url:
                            book_category = cat_name
                            break

                # Create a Book object
                book = Book(
                    title=product.get('title', "Unknown"),
                    price=price_str,
                    rating=rating,
                    availability=product.get('availability', "Unknown"),
                    category=book_category,
                    url=product.get('link', None),
                    image_url=product.get('image_url', None),
                    description=product.get('description', None)
                )

                books.append(book)

                # Add or update the category
                if book_category not in categories_dict:
                    # Get category URL from map if available
                    cat_url = cls.categories_map.get(book_category, {}).get('url',
                                                                            start_url) if cls.categories_map else start_url

                    categories_dict[book_category] = Category(
                        name=book_category,
                        url=cat_url,
                        book_count=0,
                        books=[]
                    )

                categories_dict[book_category].books.append(book)
                categories_dict[book_category].book_count += 1

            except Exception as e:
                print(f"Error processing product: {e}")
                continue

        categories = list(categories_dict.values())

        # Create a directory named after the category if scraping by category
        if category_name and categories:
            directory = os.path.join(directory, category_name.replace(" ", "_").lower())

        # Save the data
        return cls.save_all_data(books, categories, directory, formats)

    @classmethod
    def scrape_categories(cls, category_names: List[str],
                          base_url: str = "http://books.toscrape.com/",
                          max_pages_per_category: int = 3,
                          directory: str = "data",
                          formats: List[str] = ["json", "csv"]) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Scrape multiple categories and save them separately.

        Args:
            category_names: List of category names to scrape
            base_url: Base URL of the website
            max_pages_per_category: Maximum number of pages to scrape for each category
            directory: Base directory to save the files in
            formats: List of formats to save the data in ("json", "csv")

        Returns:
            Dictionary mapping category names to their saved file paths
        """
        # Make sure categories are fetched
        if not cls.categories_map:
            cls.fetch_all_categories(base_url)

        results = {}

        for category_name in category_names:
            print(f"\n=== Scraping category: {category_name} ===")
            category_result = cls.scrape_and_save(
                base_url=base_url,
                category_name=category_name,
                max_pages=max_pages_per_category,
                directory=directory,
                formats=formats
            )

            results[category_name] = category_result

        return results