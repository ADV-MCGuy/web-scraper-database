"""
scraper.py - Web scraping functionality
"""

import requests
from bs4 import BeautifulSoup
import time


def fetch_page(url):
    """
    Fetch a webpage and return the content.
    
    Args:
        url (str): The URL to fetch
        
    Returns:
        str: HTML content or None if failed
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_quotes(html):
    """
    Parse quotes from HTML.
    
    Args:
        html (str): HTML content
        
    Returns:
        list: List of dicts with 'text', 'author', 'tags'
    """
    if html is None:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []
    
    # Find all quote containers
    quote_elements = soup.find_all('div', class_='quote')
    
    for quote_elem in quote_elements:
        try:
            # Extract text
            text = quote_elem.find('span', class_='text').get_text(strip=True)
            
            # Extract author
            author_elem = quote_elem.find('small', class_='author')
            author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
            
            # Extract tags
            tag_elems = quote_elem.find_all('a', class_='tag')
            tags = [tag.get_text(strip=True) for tag in tag_elems]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': ','.join(tags)  # Store as comma-separated string
            })
        except AttributeError as e:
            print(f"Error parsing quote: {e}")
            continue
    
    return quotes


def scrape_quotes(pages=1):
    """
    Scrape quotes from toscrape.com.
    
    Args:
        pages (int): Number of pages to scrape
        
    Returns:
        list: All quotes scraped
    """
    all_quotes = []
    base_url = 'http://quotes.toscrape.com/page/'
    
    for page_num in range(1, pages + 1):
        url = f"{base_url}{page_num}/"
        print(f"Scraping page {page_num}...")
        
        html = fetch_page(url)
        if html is None:
            continue
        
        quotes = parse_quotes(html)
        all_quotes.extend(quotes)
        
        # Be respectful—wait between requests
        time.sleep(1)
    
    return all_quotes