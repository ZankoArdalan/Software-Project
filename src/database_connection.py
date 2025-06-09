import sqlite3
def create_connection():
    conn = sqlite3.connect('clothing_store.db')
    c = conn.cursor()

    # ایجاد جداول
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 role TEXT NOT NULL,
                 hourly_wage REAL DEFAULT 0,
                 monthly_salary REAL DEFAULT 0)''')

    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 description TEXT,
                 category TEXT,
                 price REAL NOT NULL,
                 stock INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 product_id INTEGER NOT NULL,
                 quantity INTEGER NOT NULL,
                 total_price REAL NOT NULL,
                 sale_date TEXT NOT NULL,
                 user_id INTEGER NOT NULL,
                 FOREIGN KEY (product_id) REFERENCES products(id),
                 FOREIGN KEY (user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS shifts (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 start_time TEXT NOT NULL,
                 end_time TEXT,
                 date TEXT NOT NULL,
                 FOREIGN KEY (user_id) REFERENCES users(id))''')

    # ایجاد کاربر پیش‌فرض
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password, role, monthly_salary) VALUES (?, ?, ?, ?)",
                  ('owner', 'owner123', 'owner', 10000000))
        c.execute("INSERT INTO users (username, password, role, monthly_salary) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin123', 'admin', 8000000))
        c.execute("INSERT INTO users (username, password, role, hourly_wage) VALUES (?, ?, ?, ?)",
                  ('staff1', 'staff123', 'staff', 50000))
        c.execute("INSERT INTO users (username, password, role, hourly_wage) VALUES (?, ?, ?, ?)",
                  ('staff2', 'staff456', 'staff', 55000))

        # افزودن محصولات نمونه
        products = [
            ('تیشرت مردانه', 'تیشرت نخی مردانه', 'لباس مردانه', 150000, 50),
            ('شلوار جین زنانه', 'شلوار جین اسلیم فیت', 'لباس زنانه', 350000, 30),
            ('کت و شلوار', 'کت و شلوار رسمی مردانه', 'لباس مردانه', 1200000, 15),
            ('دامن', 'دامن میدی زنانه', 'لباس زنانه', 280000, 25),
            ('پیراهن', 'پیراهن مجلسی زنانه', 'لباس زنانه', 450000, 20)
        ]
        c.executemany("INSERT INTO products (name, description, category, price, stock) VALUES (?, ?, ?, ?, ?)",
                      products)

    conn.commit()
    return conn