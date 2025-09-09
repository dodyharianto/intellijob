import sqlite3
from datetime import datetime, timezone, timedelta

conn = sqlite3.connect('chat_history.db')
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

def get_current_timestamp():
    utc_now = datetime.now(timezone.utc)
    utc_plus_8 = timezone(timedelta(hours=8))
    time_in_utc_plus_8 = utc_now.astimezone(utc_plus_8)
    return time_in_utc_plus_8


def add_message(role, message):
    timestamp = get_current_timestamp()

    cursor.execute("""
        INSERT INTO chat_history (role, message, timestamp)
        VALUES(?, ?, ?)
    """, (role, message, timestamp))
    conn.commit()

def get_chat_history(n_messages=5):
    # Get the last n messages
    cursor.execute("""
        SELECT role, message
        FROM chat_history
        ORDER BY id DESC
        LIMIT (?)
    """, (n_messages, ))

    last_n_chats = cursor.fetchall()
    return last_n_chats[::-1]