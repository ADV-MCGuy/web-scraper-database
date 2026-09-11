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