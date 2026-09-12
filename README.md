# Web Scraper + Database

Scrape quotes from toscrape.com and store them in a local SQLite database.

## Features
- Scrape quotes from quotes.toscrape.com
- Store in SQLite database
- Query by author, tag, or keyword
- Avoid duplicates automatically

## Setup

1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Usage

**Scrape quotes:**
```bash
python src/main.py 5  # Scrape 5 pages
```

**Query database:**
```bash
python src/query.py search love
python src/query.py author Albert
python src/query.py tag wisdom
python src/query.py all
```

## Project Structure
- `src/scraper.py` — Web scraping logic
- `src/database.py` — SQLite operations
- `src/main.py` — Scraper entry point
- `src/query.py` — Database query tool
- `data/quotes.db` — SQLite database (created at runtime)

## Favorites

Manage your favorite quotes:
```bash
# Show all favorites
python src/favorites.py show

# Search within favorites
python src/favorites.py search love

# Add quote to favorites (use ID from query results)
python src/favorites.py add 5

# Remove from favorites
python src/favorites.py remove 5

# Count favorites
python src/favorites.py count
```