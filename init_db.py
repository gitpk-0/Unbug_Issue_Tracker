import os
import psycopg2 as psycop


conn = psycop.connect(
    host="localhost",
    database="unbug_db",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('CREATE TABLE users (id SERIAL PRIMARY KEY NOT NULL,'
            'username TEXT NOT NULL,'
            'hash TEXT NOT NULL);')

# Insert data into the table
cur.execute('INSERT INTO users (id, username, hash) VALUES (%s, %s, %s)',
            (0, 'test_user', 'test_hash'))

cur.execute('INSERT INTO users (id, username, hash) VALUES (%s, %s, %s)',
            (1, 'test_user2', 'test_hash2'))

conn.commit()
cur.close()
conn.close()
