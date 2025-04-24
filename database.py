import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.create_tables()
    
    def connect(self):
        return sqlite3.connect(self.db_name, isolation_level=None)
    
    def execute(self, query, params=()):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()

    def fetchone(self, query, params=()):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchone()
        conn.close()
        return result
    
    def create_tables(self):
        """Create all tables, if they don't already exist."""
        self.execute("""
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS employment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            salary REAL,
            FOREIGN KEY (person_id) REFERENCES person(id),
            FOREIGN KEY (company_id) REFERENCES company(id)
        )
        """)

class Person:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.db = Database()

    def save(self):
        self.db.execute("INSERT INTO person (name) VALUES (?)", (self.name,))
        self.id = self.db.fetchone("SELECT last_insert_rowid()")[0]

    def remove(self):
        self.db.execute("DELETE FROM employment WHERE person_id = ?", (self.id,))
        self.db.execute("DELETE FROM person WHERE id = ?", (self.id,))

class Company:
    def __init__(self, name):
        self.id = None
        self.name = name
        self.db = Database()

    def save(self):
        self.db.execute("INSERT INTO company (name) VALUES (?)", (self.name,))
        self.id = self.db.fetchone("SELECT last_insert_rowid()")[0]

    def remove(self):
        self.db.execute("DELETE FROM employment WHERE company_id = ?", (self.id,))
        self.db.execute("DELETE FROM company WHERE id = ?", (self.id,))

class Employment:
    def __init__(self, person_id, company_id, salary):
        self.id = None
        self.person_id = person_id
        self.company_id = company_id
        self.salary = salary
        self.db = Database()

    def save(self):
        self.db.execute("INSERT INTO employment (person_id, company_id, salary) VALUES (?, ?, ?)", (self.person_id, self.company_id, self.salary))

    def remove(self):
        self.db.execute("DELETE FROM employment WHERE id = ?", (self.id,))
