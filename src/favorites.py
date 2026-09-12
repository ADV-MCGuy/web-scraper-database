"""
favorites.py - Manage favorite quotes
"""

import sys
from database import QuoteDatabase


def main():
    """Manage favorites."""
    
    db = QuoteDatabase()
    db.connect()
    
    if len(sys.argv) < 2:
        print("Favorites Manager")
        print("\nUsage:")
        print("  python src/favorites.py show              # Show all favorites")
        print("  python src/favorites.py search <keyword>  # Search favorites")
        print("  python src/favorites.py add <quote_id>    # Add to favorites")
        print("  python src/favorites.py remove <quote_id> # Remove from favorites")
        print("  python src/favorites.py count             # Show favorite count")
        db.close()
        return
    
    command = sys.argv[1]
    
    if command == 'show':
        show_favorites(db)
    
    elif command == 'search' and len(sys.argv) > 2:
        keyword = ' '.join(sys.argv[2:])
        search_favorites(db, keyword)
    
    elif command == 'add' and len(sys.argv) > 2:
        try:
            quote_id = int(sys.argv[2])
            add_favorite(db, quote_id)
        except ValueError:
            print("Error: quote_id must be a number")
    
    elif command == 'remove' and len(sys.argv) > 2:
        try:
            quote_id = int(sys.argv[2])
            remove_favorite(db, quote_id)
        except ValueError:
            print("Error: quote_id must be a number")
    
    elif command == 'count':
        count = db.get_favorite_count()
        print(f"You have {count} favorite quotes")
    
    else:
        print(f"Unknown command: {command}")
    
    db.close()


def show_favorites(db):
    """Display all favorite quotes."""
    favorites = db.get_all_favorites()
    
    if not favorites:
        print("You have no favorites yet.")
        return
    
    print(f"Your {len(favorites)} Favorite Quotes:\n")
    
    for quote_id, text, author, tags in favorites:
        print(f"[ID: {quote_id}] {text}")
        print(f"    — {author}")
        if tags:
            print(f"    Tags: {tags}")
        print()


def search_favorites(db, keyword):
    """Search favorite quotes."""
    results = db.search_favorites(keyword)
    
    if not results:
        print(f"No favorite quotes found matching '{keyword}'")
        return
    
    print(f"Found {len(results)} favorite quote(s) matching '{keyword}':\n")
    
    for quote_id, text, author, tags in results:
        print(f"[ID: {quote_id}] {text}")
        print(f"    — {author}")
        if tags:
            print(f"    Tags: {tags}")
        print()


def add_favorite(db, quote_id):
    """Add a quote to favorites."""
    success = db.add_favorite(quote_id)
    
    if success:
        total = db.get_favorite_count()
        print(f"✓ Added to favorites! (Total: {total})")
    else:
        print("This quote is already in your favorites.")


def remove_favorite(db, quote_id):
    """Remove a quote from favorites."""
    success = db.remove_favorite(quote_id)
    
    if success:
        total = db.get_favorite_count()
        print(f"✓ Removed from favorites! (Total: {total})")
    else:
        print("This quote is not in your favorites.")


if __name__ == '__main__':
    main()