from src.book_scraper.Processing import Processing


def main():
    base_url = "http://books.toscrape.com/"

    # First, fetch all available categories
    categories = Processing.fetch_all_categories(base_url)

    print("\n=== Available Categories ===")
    for name, details in categories.items():
        print(f"- {name}")

    category = input("Enter categories you want to see: ").replace(" ", "").split(",")
    for cat in category:
        if categories.__contains__(cat) is False:
            print("Wrong categories")
            return


    if len(category) == 1:
        # Example 1: Scrape a specific category
        result1 = Processing.scrape_and_save(
            base_url=base_url,
            category_name= category[0],  # Specify the category to scrape
            max_pages=2,
            directory="output_data",
            formats=["json", "csv"]
        )
    else:
        # Example 2: Scrape multiple categories at once
        result2 = Processing.scrape_categories(
            category_names=category,
            base_url=base_url,
            max_pages_per_category=1,
            directory="output_by_category",
            formats=["json"]
        )
    if len(category) == 1:
        print("\n=== Scraping Results ===")
        print(category[0] + "category:")
        for data_type, paths in result1.items():
            print(f"  {data_type}:")
            for format_type, path in paths.items():
                print(f"    - {format_type}: {path}")
    else:
        print("\nMultiple categories:")
        for category, results in result2.items():
            print(f"  {category}:")
            for data_type, paths in results.items():
                print(f"    {data_type}:")
                for format_type, path in paths.items():
                    print(f"      - {format_type}: {path}")


if __name__ == "__main__":
    main()