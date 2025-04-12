# Book Scraper Project

A comprehensive web scraping application that collects book data from [Books to Scrape](http://books.toscrape.com/), processes the information, saves it in structured formats, and performs data analysis.

## Project Overview

This web scraping application extracts detailed information about books from [Books to Scrape](http://books.toscrape.com/), including:
- Book titles
- Prices
- Ratings
- Availability
- Categories
- URLs
- Image URLs
- Descriptions

The application organizes data by categories, supports filtering, provides statistical analysis, and exports results to both JSON and CSV formats.

## Features

- **Category-Based Scraping**: Extract books from specific categories or the entire catalog
- **Pagination Support**: Navigate through multiple pages of book listings
- **Detailed Data Extraction**: Get comprehensive information about each book
- **Flexible Output**: Save data as JSON and/or CSV files
- **Data Analysis**: Perform operations like sorting, filtering, and grouping on collected data
- **Error Handling**: Robust error management for HTTP requests and parsing
- **Rate Limiting**: Respect website resources with controlled request rates

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SandroSh/scraping_project.git
cd scraping_project
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Application

Execute the main script to start the interactive scraping process:

```bash
python -m src.book_scraper.Main
```

The application will:
1. Fetch all available book categories
2. Display the categories
3. Ask you to enter one or more categories to scrape
4. Scrape books from the selected categories
5. Save the data to files
6. Perform analysis on the collected data

### Using the Processing Module Directly

For more programmatic control, you can import and use the Processing class:

```python
from src.book_scraper.Processing import Processing

# Fetch all available categories
categories = Processing.fetch_all_categories("http://books.toscrape.com/")

# Scrape a specific category
result = Processing.scrape_and_save(
    base_url="http://books.toscrape.com/",
    category_name="Mystery",
    max_pages=2,
    directory="output_data",
    formats=["json", "csv"]
)

# Scrape multiple categories
results = Processing.scrape_categories(
    category_names=["Science Fiction", "Travel", "History"],
    base_url="http://books.toscrape.com/",
    max_pages_per_category=1,
    directory="output_by_category",
    formats=["json"]
)

# Analyze collected data
books = Processing.load_all_books_from_folder("output_data")
top_rated = Processing.get_top_n_books_by_rating(books, 5)
high_rated = Processing.filter_books_by_min_rating(books, 4.5)
by_category = Processing.group_books_by_category(books)
```

## Project Structure

```
book_scraper/
├── models/             # Data models for books and categories
│   ├── __init__.py
│   ├── book.py         # Book class definition
│   └── category.py     # Category class definition
├── output_data/        # Directory for scraped data output
├── __init__.py
├── Main.py             # Main entry point script
├── parser.py           # HTML parsing functions
├── Processing.py       # Data processing and storage functions
├── requests_module/    # HTTP request handling
│   ├── __init__.py
│   ├── error_handler.py    # HTTP error handling
│   └── requests_manager.py # Request execution with retries
└── Utils/              # Utility functions
    ├── __init__.py
    └── utils.py        # URL handling, extraction helpers
```

## Data Models

### Book
Represents a book with properties:
- title
- price
- rating
- availability
- category
- url
- image_url
- description

### Category
Represents a book category with properties:
- name
- url
- book_count
- books (list of Book objects)

## Robots.txt Compliance

The application respects the [Books to Scrape robots.txt](http://books.toscrape.com/robots.txt) policy. The website is specifically designed for scraping practice and doesn't impose restrictions, but our implementation includes:

- User-agent identification
- Rate limiting
- Error handling to prevent server overload

## Data Analysis Features

The application supports various data analysis operations:

- **Top Books**: Get the highest rated books
- **Rating Filters**: Find books with ratings above a threshold
- **Category Grouping**: Organize books by their categories
- **Average Rating**: Calculate mean ratings across books
- **Title Search**: Find books with specific text in their titles
- **Price Filtering**: Find books in specific price ranges
- **Extreme Values**: Identify cheapest and most expensive books


