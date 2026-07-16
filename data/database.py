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
                reading TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'pending',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );""")
        self.conn.commit()


    def add_word(self, word):
        try:
            sql = 'INSERT INTO vocabulary (reading) VALUES (?)'
            self.cursor.execute(sql, (word,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass


    def remove_word(self, word):
        sql = 'DELETE FROM vocabulary WHERE reading = ?'
        self.cursor.execute(sql, (word,))
        self.conn.commit()


    def get_all_words(self):
        sql = 'SELECT id, reading, status, timestamp FROM vocabulary'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    
    def get_incomplete_words(self):
        sql = 'SELECT reading FROM vocabulary WHERE status IN ("processing", "pending", "skipped")'
        self.cursor.execute(sql)
        return self.cursor.fetchall()


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

        elif status == "processing":
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('processing', word))
            self.conn.commit()
        
        elif status == "already in deck":
            sql = 'UPDATE vocabulary SET status = ? WHERE reading = ?'
            self.cursor.execute(sql, ('already in deck', word))
            self.conn.commit()
            

    def close(self):
        self.conn.close()
