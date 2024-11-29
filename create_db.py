import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('users.db')

# Execute the SQL command to create the table
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        bio TEXT
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup complete!")
