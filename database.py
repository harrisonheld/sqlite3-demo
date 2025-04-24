import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()
        self.create_tables()
    
    def execute(self, query, params=()):
        self.cur.execute(query, params)
        self.conn.commit()

    def fetchone(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchone()

    def create_tables(self):
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

    def close(self):
        self.conn.close()


db = Database()

class Person:
    def __init__(self, name):
        self.id = None
        self.name = name

    def save(self):
        db.execute("INSERT INTO person (name) VALUES (?)", (self.name,))
        self.id = db.fetchone("SELECT last_insert_rowid()")[0]

    def remove(self):
        db.execute("DELETE FROM employment WHERE person_id = ?", (self.id,))
        db.execute("DELETE FROM person WHERE id = ?", (self.id,))

class Company:
    def __init__(self, name):
        self.id = None
        self.name = name

    def save(self):
        db.execute("INSERT INTO company (name) VALUES (?)", (self.name,))
        self.id = db.fetchone("SELECT last_insert_rowid()")[0]

    def remove(self):
        db.execute("DELETE FROM employment WHERE company_id = ?", (self.id,))
        db.execute("DELETE FROM company WHERE id = ?", (self.id,))

class Employment:
    def __init__(self, person_id, company_id, salary):
        self.id = None
        self.person_id = person_id
        self.company_id = company_id
        self.salary = salary

    def save(self):
        db.execute("INSERT INTO employment (person_id, company_id, salary) VALUES (?, ?, ?)", (self.person_id, self.company_id, self.salary))
        self.id = db.fetchone("SELECT last_insert_rowid()")[0]

    def remove(self):
        db.execute("DELETE FROM employment WHERE id = ?", (self.id,))

    def print(self):
        person = db.fetchone("SELECT name FROM person WHERE id = ?", (self.person_id,))
        company = db.fetchone("SELECT name FROM company WHERE id = ?", (self.company_id,))
        if person and company:
            print(f"Person: {person[0]}")
            print(f"Company: {company[0]}")
            print(f"Salary: ${self.salary}")
        else:
            print("Employment data not found!")
