import sqlite3

# create a function because do not repeat a code
def db_connect():
    return sqlite3.connect("grocery.db")

# start a program to create a table automatically

def create_table():
    # using with function it can create automatically and after close it.
    with db_connect() as connect:
        # cursor : it is use to execute a sql quary.
        cur = connect.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price REAL,
            quantity INTEGER
            )
            """)

        cur.execute("""
           CREATE TABLE IF NOT EXISTS sales(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           product_name TEXT,
           quantity INTEGER,
           total REAL,
           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
             """)

create_table()
