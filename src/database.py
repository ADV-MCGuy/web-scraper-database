"""
database.py - SQLite database operations
"""

import sqlite3
from datetime import datetime


class QuoteDatabase:
    """Handle all database operations for quotes."""
    
    def __init__(self, db_path='data/quotes.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to database and create tables if needed."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self._create_tables()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def _create_tables(self):
        """Create tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                text TEXT UNIQUE NOT NULL,
                author TEXT NOT NULL,
                tags TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Favorites table - link to quotes"
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY,
                quote_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()
    
    def insert_quotes(self, quotes):
        """
        Insert quotes into database.
        
        Args:
            quotes (list): List of quote dicts
            
        Returns:
            int: Number of quotes inserted
        """
        inserted = 0
        
        for quote in quotes:
            try:
                self.cursor.execute('''
                    INSERT INTO quotes (text, author, tags)
                    VALUES (?, ?, ?)
                ''', (quote['text'], quote['author'], quote['tags']))
                inserted += 1
            except sqlite3.IntegrityError:
                # Quote already exists, skip
                continue
        
        self.conn.commit()
        return inserted
    
    def get_quotes_by_author(self, author):
        """Get all quotes by an author."""
        self.cursor.execute('''
            SELECT text, author, tags FROM quotes WHERE author LIKE ?
        ''', (f'%{author}%',))
        return self.cursor.fetchall()
    
    def get_quotes_by_tag(self, tag):
        """Get all quotes with a specific tag."""
        self.cursor.execute('''
            SELECT text, author, tags FROM quotes WHERE tags LIKE ?
        ''', (f'%{tag}%',))
        return self.cursor.fetchall()
    
    def search_quotes(self, keyword):
        """Search quotes by text."""
        self.cursor.execute('''
            SELECT text, author, tags FROM quotes WHERE text LIKE ?
        ''', (f'%{keyword}%',))
        return self.cursor.fetchall()
    
    def get_all_quotes(self):
        """Get all quotes from database."""
        self.cursor.execute('SELECT text, author, tags FROM quotes')
        return self.cursor.fetchall()
    
    def get_quote_count(self):
        """Get total number of quotes."""
        self.cursor.execute('SELECT COUNT(*) FROM quotes')
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def add_favorite(self, quote_id):
        """ 
        Add a quote to favorites.
        
        Args:
            quote_id (int): ID of the quote to add to favorites
        
        Returns:
            bool: True if added, False if already exists
        """
        try:
            self.cursor.execute('''
                INSERT INTO favorites (quote_id) VALUES (?)
            ''', (quote_id,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Quote already in favorites
            return False

    def remove_favorite(self, quote_id):
        """ 
        Remove a quote from favorites.
        
        Args:
            quote_id (int): ID of the quote to remove from favorites
        
        Returns:
            bool: True if removed, False if not found
        """
        self.cursor.execute('''
            DELETE FROM favorites WHERE quote_id = ?
        ''', (quote_id,))

        deleted = self.conn.total_changes > 0
        self.conn.commit()
        return deleted

    def get_all_favorites(self):
        """
        Get all favorite quotes.

        Returns:
            list: List of favorite quotes with their details
        """
        self.cursor.execute('''
            SELECT q.id, q.text, q.author, q.tags
            FROM quotes q
            INNER JOIN favorites f ON q.id = f.quote_id
            ORDER BY f.added_at DESC
        ''')
        return self.cursor.fetchall()

    def search_favorites(self, keyword):
        """
        Search favorite quotes by text.

        Args:
            keyword (str): Keyword to search in favorite quotes

        Returns:
            list: List of matching favorite quotes
        """
        self.cursor.execute('''
            SELECT q.id, q.text, q.author, q.tags
            FROM quotes q
            INNER JOIN favorites f ON q.id = f.quote_id
            WHERE q.text LIKE ?
            ORDER BY f.added_at DESC
        ''', (f'%{keyword}%',))
        return self.cursor.fetchall()

    def is_favorited(self, quote_id):
        """
        Check if a quote is in favorites.

        Args:
            quote_id (int): ID of the quote to check
        
        Returns:
            bool: True if favorited
        """
        self.cursor.execute('''
            SELECT 1 FROM favorites WHERE quote_id = ?
        ''', (quote_id,))
        return self.cursor.fetchone() is not None

    def get_favorite_count(self):
        """
        Get total number of favorite quotes.

        Returns:
            int: Count of favorite quotes
        """
        self.cursor.execute('SELECT COUNT(*) FROM favorites')
        return self.cursor.fetchone()[0]

    