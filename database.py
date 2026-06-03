import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="cryptyumy.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_requests INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                last_checkin DATE,
                charts_generated INTEGER DEFAULT 0,
                friends_invited INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()
    
    def add_or_update_user(self, user_id, username, first_name):
        self.cursor.execute("""
            INSERT INTO users (user_id, username, first_name, last_active, total_requests)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_active = CURRENT_TIMESTAMP,
                total_requests = total_requests + 1
        """, (user_id, username, first_name))
        self.conn.commit()
    
    def add_xp(self, user_id, amount):
        self.cursor.execute(
            "UPDATE users SET xp = xp + ? WHERE user_id = ?",
            (amount, user_id)
        )
        self.conn.commit()
    
    def get_user_stats(self, user_id):
        self.cursor.execute(
            "SELECT xp, level, streak, charts_generated, friends_invited FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchone()
        if result:
            return {
                "xp": result[0],
                "level": result[1],
                "streak": result[2],
                "charts": result[3],
                "friends": result[4]
            }
        return None
    
    def get_total_users(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        return self.cursor.fetchone()[0]
    
    def close(self):
        self.conn.close()
