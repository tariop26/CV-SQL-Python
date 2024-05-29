import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('cv_database.db')
cursor = conn.cursor()

# Read the SQL script
with open('create_cv_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
cursor.executescript(sql_script)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and initialized successfully.")
