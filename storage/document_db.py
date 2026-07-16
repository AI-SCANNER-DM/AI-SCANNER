import sqlite3


class DocumentDatabase:

    def __init__(self):
        self.connection = sqlite3.connect("storage/scanner.db")
        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT

        )
        """)

        self.connection.commit()

    def save_document(self, title, content, date):

        self.cursor.execute("""
        INSERT INTO documents(title, content, date)
        VALUES (?, ?, ?)
        """, (title, content, date))

        self.connection.commit()

    def get_all_documents(self):

        self.cursor.execute("SELECT * FROM documents")

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()