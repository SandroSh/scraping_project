from src.book_scraper.Processing import Processing


def main():
    base_url = "http://books.toscrape.com/"

    # First, fetch all available categories
    # categories = Processing.fetch_all_categories(base_url)
    #
    # print("\n=== Available Categories ===")
    # for name, details in categories.items():
    #     print(f"- {name}")
    #
    # category = input("Enter categories you want to see: ").replace(" ", "").split(",")
    # for cat in category:
    #     if categories.__contains__(cat) is False:
    #         print("Wrong categories")
    #         return
    #
    #
    # if len(category) == 1:
    #     # Example 1: Scrape a specific category
    #     result1 = Processing.scrape_and_save(
    #         base_url=base_url,
    #         category_name= category[0],  # Specify the category to scrape
    #         max_pages=2,
    #         directory="output_data",
    #         formats=["json", "csv"]
    #     )
    # else:
    #     # Example 2: Scrape multiple categories at once
    #     result2 = Processing.scrape_categories(
    #         category_names=category,
    #         base_url=base_url,
    #         max_pages_per_category=1,
    #         directory="output_by_category",
    #         formats=["json"]
    #     )
    # if len(category) == 1:
    #     print("\n=== Scraping Results ===")
    #     print(category[0] + "category:")
    #     for data_type, paths in result1.items():
    #         print(f"  {data_type}:")
    #         for format_type, path in paths.items():
    #             print(f"    - {format_type}: {path}")
    # else:
    #     print("\nMultiple categories:")
    #     for category, results in result2.items():
    #         print(f"  {category}:")
    #         for data_type, paths in results.items():
    #             print(f"    {data_type}:")
    #             for format_type, path in paths.items():
    #                 print(f"      - {format_type}: {path}")

all_books = Processing.load_all_books_from_folder("output_data")

print("Top 5 rated books:")
Top5Books = Processing.get_top_n_books_by_rating(all_books, 5)

for book in Top5Books:
    print(book.get("title"))
    print(book.get("rating"))
    print("-" * 50)

print("\nBooks with rating >= 4.5:")
print(Processing.filter_books_by_min_rating(all_books, 4.5))

print("\nGrouped by category:")
print(Processing.group_books_by_category(all_books))

print("\nAverage rating:")
print(Processing.average_rating(all_books))

print("\nBooks per category:")
print(Processing.books_per_category(all_books))

print("\nSearch for title containing 'mystery':")
print(Processing.search_by_title(all_books, 'mystery'))

print("\nBooks priced between 10 and 30:")
print(Processing.in_price_range(all_books, 10, 30))

print("\nTop 5 most expensive books:")
print(Processing.top_expensive(all_books))

print("\nTop 5 cheapest books:")
print(Processing.top_cheap(all_books))

print("\nBooks missing required info:")
print(Processing.missing_info(all_books))


if __name__ == "__main__":
    main()