from bs4 import BeautifulSoup
from src.requests_module.requests_manager import get_request
from src.Utils import absolute_url, extract_number


def parse_html(html_content):
    try:
        if not html_content:
            raise ValueError("HTML content is empty or None.")

        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Failed to parse HTML content: {str(e)}")
        return None


def scrape_links(soup, url):
    try:
        if not soup:
            raise ValueError("Invalid BeautifulSoup object. Cannot scrape products.")

        image_divs = soup.find_all('div', class_='image_container')
        if not image_divs:
            raise ValueError("No product items found with the specified classes.")

        links = []
        for div in image_divs:
            try:
                link_tag = div.find('a')
                href = link_tag['href'].strip() if link_tag and 'href' in link_tag.attrs else None
                if href:
                    links.append(absolute_url(base_url=url, relative_url=href))
            except Exception as e:
                print(f"Error scraping product item: {str(e)}. Skipping this item.")
                continue

        return links

    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []


def scrape_products(soup):
    try:
        if not soup:
            raise ValueError("Invalid BeautifulSoup object. Cannot scrape products.")

        product_item = soup.find('article', class_='product_page')
        if not product_item:
            raise ValueError("No product items found with the specified classes.")

        # Extract title
        title_tag = product_item.find('h1')
        title = title_tag.text.strip() if title_tag else "Title not found"

        # Extract price
        price_tag = product_item.find('p', class_='price_color')
        price = price_tag.text.strip()[1:]

        # Extract description
        description_tag = product_item.find('div', id='product_description')
        description = description_tag.find_next('p').text.strip() if description_tag else "Description not found"

        # Extract table data
        table = product_item.find('table', class_='table-striped')
        rows = table.find_all('tr') if table else []

        upc = rows[0].find('td').text if len(rows) > 0 else 'UPC not found'
        product_type = rows[1].find('td').text if len(rows) > 1 else 'Type not found'
        availability = rows[5].find('td').text if len(rows) > 5 else 'Availability not found'
        review_count = rows[6].find('td').text if len(rows) > 6 else '0'

        product = {
            'title': title,
            'price': price,
            'description': description,
            'upc': upc,
            'type': product_type,
            'availability': extract_number(availability),
            'review_count': int(review_count)
        }

        return product

    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return None


def scrape_products_with_details(links):
    try:
        if not links:
            raise ValueError("Empty links list provided.")

        products = []
        for link in links:
            try:
                response = get_request(link)
                if response:
                    soup = parse_html(response.text)
                    product = scrape_products(soup)
                    if product:
                        products.append(product)
            except Exception as e:
                print(f"Error scraping {link}: {str(e)}. Skipping this item.")
                continue

        return products

    except ValueError as ve:
        print(f"Error: {ve}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []


if __name__ == "__main__":
    base_url = "https://books.toscrape.com/"

    # Get main page
    response = get_request(base_url)
    if not response:
        print("Failed to fetch main page")
        exit(1)

    # Parse and scrape
    soup = parse_html(response.text)
    if not soup:
        print("Failed to parse main page")
        exit(1)

    links = scrape_links(soup, base_url)
    if not links:
        print("No links found")
        exit(1)

    products = scrape_products_with_details(links[:5])  # Limit to 5 for testing
    for product in products:
        print(product)

