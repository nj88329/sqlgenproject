import sqlite3

#  Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('companies.db')

# create a cursor object to interact with the database
cursor = conn.cursor()


# 🔥 FORCE recreate table
cursor.execute("DROP TABLE IF EXISTS companies")
# Create a table to store company information

cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY ,
    name TEXT  NOT NULL,
    employee VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    UNIQUE(name, employee, department)
);
''')

    # Data to insert
companies = [
        ('Google', 'Alice', 'Engineering'),
        ('X', 'Bob', 'Marketing'),
        ('Microsoft', 'Charlie', 'Engineering'),
        ('Tesla', 'David', 'Sales'),
        ('Amazon', 'Eve', 'Logistics')
    ]

   # Insert data safely (no duplicates)
cursor.executemany('''
    INSERT OR IGNORE INTO companies (name, employee, department)
    VALUES (?, ?, ?)
    ''', companies)

    # Fetch and display data
cursor.execute('SELECT * FROM companies')
rows = cursor.fetchall()

print("\n📊 Company Data:\n")
for row in rows:
    print(row)


# Commit the changes and close the connection
conn.commit()
conn.close()

