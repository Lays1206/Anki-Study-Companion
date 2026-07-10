import sqlite3


class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.create_tables()
 

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY,
                reading TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );""")
        self.conn.commit()


    def add_word(self, word):
        sql = 'INSERT INTO vocabulary (reading) VALUES (?)'
        self.cursor.execute(sql, (word,))
        self.conn.commit()


    def update_status(self, word, status):
        if status == "completed":
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('completed', word))
            self.conn.commit()

        elif status == "skipped":
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('skipped', word))
            self.conn.commit()

        elif status == "pending":
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('pending', word))
            self.conn.commit()

        else:
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('processing', word))
            self.conn.commit()


    def close(self):
        self.conn.close()
