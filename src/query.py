"""
query.py - Query the quotes database
"""

import sys
from database import QuoteDatabase


def main():
    """Query the database for quotes."""
    
    db = QuoteDatabase()
    db.connect()
    
    if len(sys.argv) > 1:
        search_type = sys.argv[1]
        search_term = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
    else:
        print("Query Options:")
        print("  python src/query.py search <keyword>")
        print("  python src/query.py author <author>")
        print("  python src/query.py tag <tag>")
        print("  python src/query.py all")
        db.close()
        return
    
    results = []
    
    if search_type == 'search':
        results = db.search_quotes(search_term)
        print(f"Search results for '{search_term}':")
    elif search_type == 'author':
        results = db.get_quotes_by_author(search_term)
        print(f"Quotes by {search_term}:")
    elif search_type == 'tag':
        results = db.get_quotes_by_tag(search_term)
        print(f"Quotes with tag '{search_term}':")
    elif search_type == 'all':
        results = db.get_all_quotes()
        print(f"All {len(results)} quotes:")
    else:
        print(f"Unknown search type: {search_type}")
    
    if not results:
        print("No results found.")
    else:
        for i, (text, author, tags) in enumerate(results, 1):
            print(f"\n{i}. {text}")
            print(f"   — {author}")
            if tags:
                print(f"   Tags: {tags}")
    
    db.close()


if __name__ == '__main__':
    main()