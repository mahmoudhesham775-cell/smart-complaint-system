import sqlite3

def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'مجهول',
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()
    print("Database created successfully!")

init_db()