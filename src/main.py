"""
main.py - Entry point for web scraper
"""

import sys
from scraper import scrape_quotes
from database import QuoteDatabase


def main():
    """Main function to scrape and store quotes."""
    
    # Get number of pages to scrape
    if len(sys.argv) > 1:
        try:
            pages = int(sys.argv[1])
        except ValueError:
            pages = 1
    else:
        pages = int(input("How many pages to scrape? (default: 1): ") or "1")
    
    print(f"Starting to scrape {pages} page(s)...")
    
    # Scrape quotes
    quotes = scrape_quotes(pages=pages)
    
    if not quotes:
        print("No quotes scraped.")
        return
    
    print(f"Scraped {len(quotes)} quotes")
    
    # Store in database
    db = QuoteDatabase()
    db.connect()
    
    inserted = db.insert_quotes(quotes)
    print(f"Inserted {inserted} new quotes into database")
    
    total = db.get_quote_count()
    print(f"Database now contains {total} total quotes")
    
    db.close()
    
    print("Done!")


if __name__ == '__main__':
    main()