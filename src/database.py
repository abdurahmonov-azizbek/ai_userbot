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

def add_source(username: str):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("INSERT OR REPLACE INTO sources VALUES (?, CURRENT_TIMESTAMP)", (username,))
    conn.commit()
    conn.close()

def get_all_sources():
    """Get all source channels/groups"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sources ORDER BY added_at DESC")
    sources = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sources

def del_source(username: str):
    """Remove a source channel/group"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("DELETE FROM sources WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def set_target_chat(username: str):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("DELETE FROM target_chat")  # Clear previous
    conn.execute("INSERT INTO target_chat VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_target_chat():
    """Get current target channel"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM target_chat LIMIT 1")
    target = cursor.fetchone()
    conn.close()
    return target[0] if target else None

def enable_ai():
    """Enable AI message processing"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("UPDATE ai_settings SET is_enabled = 1 WHERE id = 1")
    conn.commit()
    conn.close()

def disable_ai():
    """Disable AI message processing"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("UPDATE ai_settings SET is_enabled = 0 WHERE id = 1")
    conn.commit()
    conn.close()

def set_ai_model(model: str):
    """Change active AI model"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("UPDATE ai_settings SET model = ? WHERE id = 1", (model,))
    conn.commit()
    conn.close()

def get_ai_status():
    """Get current AI settings"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT model, is_enabled FROM ai_settings WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return {
        'model': result[0],
        'enabled': bool(result[1])
    } if result else None