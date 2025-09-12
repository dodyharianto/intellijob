import sqlite3
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
chat_history_db = os.environ.get("CHAT_HISTORY_DB")

def create_chat_history():
    conn = sqlite3.connect(chat_history_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
        """)

    conn.commit()
    conn.close()

def get_current_timestamp():
    utc_now = datetime.now(timezone.utc)
    utc_plus_8 = timezone(timedelta(hours=8))
    time_in_utc_plus_8 = utc_now.astimezone(utc_plus_8)
    return time_in_utc_plus_8

def add_message(role, message):
    timestamp = get_current_timestamp()

    conn = sqlite3.connect(chat_history_db)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (role, message, timestamp)
        VALUES(?, ?, ?)
    """, (role, message, timestamp))

    conn.commit()
    conn.close()

def get_chat_history(n_messages=5):
    conn = sqlite3.connect(chat_history_db)
    cursor = conn.cursor()

    # Get the last n messages
    cursor.execute("""
        SELECT role, message
        FROM chat_history
        ORDER BY id DESC
        LIMIT (?)
    """, (n_messages, ))

    last_n_chats = cursor.fetchall()
    conn.commit()
    conn.close()
    return last_n_chats[::-1]