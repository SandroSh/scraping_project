from bs4 import BeautifulSoup, Tag
from src.requests_module.requests_manager import get_request
from src.Utils.utils import absolute_url, extract_number


def parse_html(html_content):
    try:
        if not html_content:
            raise ValueError("HTML content is empty or None.")
        return BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        print(f"Failed to parse HTML content: {e}")
        return None

# --- Modular extraction methods ---
def select_with_css(soup, selector):
    try:
        return [el.get_text(strip=True) for el in soup.select(selector) if isinstance(el, Tag)]
    except Exception as e:
        print(f"CSS selector error: {e}")
        return []

def select_with_tag_and_attr(soup, tag, attr_name=None, attr_value=None):
    try:
        if attr_name and attr_value:
            elements = soup.find_all(tag, {attr_name: attr_value})
        else:
            elements = soup.find_all(tag)
        return [el.get_text(strip=True) for el in elements if isinstance(el, Tag)]
    except Exception as e:
        print(f"Tag + attribute selection error: {e}")
        return []

def recursive_text_extraction(element, depth=0, max_depth=5):
    if depth > max_depth or not element:
        return []
    results = []
    for child in element.children:
        if isinstance(child, Tag):
            text = child.get_text(strip=True)
            if text:
                results.append(text)
            results.extend(recursive_text_extraction(child, depth + 1, max_depth))
    return results

def extract_description(detail_url):
    try:
        response = get_request(detail_url)
        if not response or not hasattr(response, 'text'):
            return "Description not available"
        soup = parse_html(response.text)
        if not soup:
            return "Description not available"
        desc_header = soup.find('div', id='product_description')
        if desc_header:
            desc_paragraph = desc_header.find_next_sibling('p')
            return desc_paragraph.get_text(strip=True) if desc_paragraph else "Description not found"
        return "Description not found"
    except Exception as e:
        print(f"Error extracting description from {detail_url}: {e}")
        return "Description error"

def extract_product_details(soup, base_url):
    products = []
    try:
        product_articles = soup.select('article.product_pod')
        if not product_articles:
            raise ValueError("No product articles found.")

        for article in product_articles:
            try:
                title_tag = article.select_one('h3 a')
                title = title_tag['title'] if title_tag and 'title' in title_tag.attrs else "Title not found"
                relative_link = title_tag.get("href", "")
                if 'catalogue/' not in relative_link:
                    relative_link = 'catalogue/' + relative_link
                full_link = absolute_url(base_url, relative_link) if relative_link else "Link not found"

                price = select_with_css(article, '.price_color')
                image = article.find('img')
                image_url = absolute_url(base_url, image['src']) if image and 'src' in image.attrs else "Image not found"

                availability_list = select_with_tag_and_attr(article, 'p', 'class', 'instock availability')
                availability_text = availability_list[0] if availability_list else "Availability not found"

                description = extract_description(full_link)

                rating_tag = article.select_one('p.star-rating')
                rating_map = {
                    'One': 1, 'Two': 2, 'Three': 3,
                    'Four': 4, 'Five': 5
                }
                rating = 0
                if rating_tag:
                    for cls in rating_tag.get('class', []):
                        if cls in rating_map:
                            rating = rating_map[cls]
                            break

                product_data = {
                    'title': title,
                    'price': price[0].replace("Â", "") if price else "Price not found",
                    'link': full_link,
                    'image_url': image_url,
                    'availability': availability_text,
                    'description': description,
                    'rating': rating  # Add this line
                }

                products.append(product_data)
            except Exception as inner_e:
                print(f"Error extracting product info: {inner_e}")
                continue
    except Exception as e:
        print(f"Main product extraction error: {e}")
    return products

def get_next_page_url(soup, current_url):
    next_li = soup.find('li', class_='next')
    if next_li:
        next_link = next_li.find('a')
        if next_link and next_link.get('href'):
            return absolute_url(current_url, next_link['href'])
    return None

def scrape_all_pages(base_url):
    all_products = []
    next_page = base_url
    a = 0
    while next_page and a < 1:
        a+=1
        print(f"Fetching page: {next_page}")
        response = get_request(next_page)
        if not response or not hasattr(response, 'text'):
            print(f"Failed to fetch {next_page}")
            break

        soup = parse_html(response.text)
        if not soup:
            break

        page_products = extract_product_details(soup, base_url)
        all_products.extend(page_products)

        next_page = get_next_page_url(soup, next_page)

    return all_products

def main():
    base_url = "http://books.toscrape.com/"
    products = scrape_all_pages(base_url)
    print("\n--- Extracted Product Details ---")
    for product in products:
        for key, value in product.items():
            print(f"{key}: {value}")
        print("-" * 50)

if __name__ == "__main__":
    main()

