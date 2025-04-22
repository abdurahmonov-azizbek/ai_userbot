import sqlite3
from config import DATABASE_NAME

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Simplified schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        username TEXT PRIMARY KEY,  -- Using @username instead of chat_id
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS target_chat (
        username TEXT PRIMARY KEY  -- Single target chat storage
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spam_keywords (
        keyword TEXT PRIMARY KEY
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spam_types (
        type TEXT PRIMARY KEY  -- 'photo', 'video', etc.
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),  -- Single row enforcement
        model TEXT NOT NULL DEFAULT 'gpt-3.5-turbo',
        is_enabled BOOLEAN NOT NULL DEFAULT 0
    )
    """)
    
    # Initialize AI settings with default values
    cursor.execute("""
    INSERT OR IGNORE INTO ai_settings (id, model, is_enabled)
    VALUES (1, ?, 0)
    """, ("gpt-3.5-turbo",))
    
    conn.commit()
    conn.close()

def get_sources():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM sources")
    sources = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sources

def add_source(chat_id, title):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO sources VALUES (?, ?)", (chat_id, title))
    conn.commit()
    conn.close()

def remove_source(chat_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sources WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

# Similar functions for keywords, spam_types, and settings...
# [Additional database functions would go here]