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
cur.execute('DROP TABLE IF EXISTS issues')
cur.execute('DROP TABLE IF EXISTS users')

cur.execute('CREATE TABLE users (id SERIAL PRIMARY KEY NOT NULL,'
            'username TEXT NOT NULL,'
            'hash TEXT NOT NULL);')

cur.execute('CREATE TABLE issues (user_id SERIAL NOT NULL,'
            'subject TEXT NOT NULL,'
            'summary TEXT NOT NULL,'
            'reporter TEXT NOT NULL,'
            'date_time TEXT NOT NULL,'
            'status TEXT NOT NULL,'
            'priority TEXT NOT NULL,'
            'issue_num SERIAL NOT NULL,'
            'comments TEXT,'
            'CONSTRAINT fk_issues FOREIGN KEY(user_id) REFERENCES users(id));')

# # Insert data into the table
# cur.execute('INSERT INTO users (id, username, hash) VALUES (%s, %s, %s)',
#             (0, 'test_user', 'test_hash'))

# cur.execute('INSERT INTO users (id, username, hash) VALUES (%s, %s, %s)',
#             (1, 'test_user2', 'test_hash2'))

conn.commit()
cur.close()
conn.close()
