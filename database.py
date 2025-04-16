import sqlite3

conn = sqlite3.connect('products.db', check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        xpath TEXT,
        price REAL);""") 
    conn.commit()

create_table()

def insert(product):
    sql = """INSERT INTO product(title, url, xpath, price) VALUES(?,?,?,?)"""
    try:
        with conn:
            cursor.execute(sql, product)
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных: {e}")
        return None