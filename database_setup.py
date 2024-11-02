import mysql.connector
import hashlib
import random
import os


db_config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'host': os.environ.get('DB_HOST', 'db'),
    'database': os.environ.get('DB_NAME', 'news_db')
}


def get_db_connection():
    return mysql.connector.connect(**db_config)

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            publish_date DATE NOT NULL,
            views INT DEFAULT 0,
            image_url VARCHAR(255),
            content TEXT NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flag (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flag_data VARCHAR(255) NOT NULL
        )
    ''')


    cursor.execute("SELECT COUNT(*) FROM news")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO news (title, author, category, publish_date, views, image_url, content) VALUES
            ('Sample News 1', 'Author 1', 'Category 1', '2024-01-01', 100, NULL, 'This is the content of sample news 1.'),
            ('Sample News 2', 'Author 2', 'Category 2', '2024-02-01', 200, NULL, 'This is the content of sample news 2.')
        ''')


    cursor.execute("SELECT COUNT(*) FROM flag")
    if cursor.fetchone()[0] == 0:

        random_value = str(random.random()).encode('utf-8')
        random_hash = hashlib.sha256(random_value).hexdigest()
        cursor.execute("INSERT INTO flag (flag_data) VALUES (%s)", (random_hash,))

    conn.commit()
    cursor.close()
    conn.close()
