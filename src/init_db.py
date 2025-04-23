import sqlite3
from config import Config

conn = sqlite3.connect(Config.DATABASE_NAME)
cursor = conn.cursor()
    
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