from bs4 import BeautifulSoup
from requests_module import fetch_webpage
from utils import absolute_url
from utils import extract_number, save_list_to_csv_and_json


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
                href = link_tag['href'].strip() if link_tag and 'href' in link_tag.attrs else "Href not found"
            
                links.append(absolute_url(base_url=url, relative_url=href))
                
            except Exception as e:
                print(f"Error scraping product item: {str(e)}. Skipping this item.")
                continue
            
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []
    return links

