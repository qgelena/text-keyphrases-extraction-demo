import sqlite3

SCHEMA = [
'''
CREATE TABLE IF NOT EXISTS Texts (
    text TEXT NOT NULL     -- TODO: maybe unique;
);
''',
'''
CREATE TABLE IF NOT EXISTS Keyphrases (
    keyphrase TEXT NOT NULL UNIQUE,
    wikilink TEXT 
);
''',
'''
CREATE TABLE IF NOT EXISTS TextKeyphrases (
    text_id INT NOT NULL,   
    keyphrase_id INT NOT NULL,
    relevance REAL NOT NULL
);
''']

class Database:
    def __init__(self, dbpath):
        # connect to the database;
        self.conn = sqlite3.connect(dbpath, check_same_thread=False)

        # check its schema and create tables if needed;
        for table in SCHEMA:
            self.conn.execute(table)
        self.conn.commit()

    def save_text(self, text):
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO Texts (text) VALUES (?)',
            [text])
        cur.connection.commit()
        return cur.lastrowid
    
    def get_text(self, id):
        cur = self.conn.cursor()
        cur.execute('SELECT text FROM Texts WHERE rowid=?', (id,))
        text = cur.fetchone()[0]  # =>  ('hgkggkjhjkgjhg',)
        cur.close()
        return text
    
    def save_keywords(self, text_id, keywords):
        cur = self.conn.cursor()
        pairs = []
        
        for keyphrase, relevance in keywords:
            try:
                cur.execute('INSERT INTO Keyphrases (keyphrase) VALUES (?)', [keyphrase])
                cur.connection.commit()
                pairs.append((text_id, cur.lastrowid, relevance))
            except sqlite3.IntegrityError:
                cur.execute('SELECT rowid FROM Keyphrases WHERE keyphrase = ?', [keyphrase])
                keyphrase_id = cur.fetchone()[0]
                pairs.append((text_id, keyphrase_id, relevance))
        cur.executemany(
            'INSERT INTO TextKeyphrases(text_id, keyphrase_id, relevance) VALUES(?, ?, ?)',
            pairs
        )
        self.conn.commit()
    
    def get_keywords(self, text_id):
        query = '''SELECT k.keyphrase, tk.relevance, k.wikilink
        FROM TextKeyphrases tk 
        LEFT JOIN Keyphrases k ON tk.keyphrase_id = k.rowid
        WHERE tk.text_id = ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(query, (text_id,))
            return cur.fetchall()
        finally:
            cur.close()

if __name__ == '__main__':
    db = Database('ProphyTest.db')
    keywords = [
        ('grapefruit', 42),
        ('orange', 26),
        ('banana', 21),
    ]
    db.save_keywords(17, keywords)
    