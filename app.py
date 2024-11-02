from flask import Flask, request, redirect, render_template_string
import mysql.connector
import os

from database_setup import setup_database

app = Flask(__name__)


db_config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'host': os.environ.get('DB_HOST', 'db'),
    'database': os.environ.get('DB_NAME', 'news_db')
}



def get_db_connection():
    return mysql.connector.connect(**db_config)

setup_database()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title FROM news")
    news_list = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/global.css">
        <title>News List - Voorivex Academy</title>
    </head>
    <body>
        <h1>News List</h1>
        <ul>
            {% for news in news_list %}
                <li><a href="/post?id={{ news['id'] }}">{{ news['title'] }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html_template, news_list=news_list)



@app.route('/post')
def post():
    news_id = request.args.get('id')
    if not news_id:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    sql = f"SELECT * FROM news WHERE id = '{news_id}'"
    cursor.execute(sql)
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    if not post:
        return "<h1>Article Not Found</h1>"

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/global.css">
        <title>{{ post['title'] }} - Voorivex Academy</title>
    </head>
    <body>
        <a href="/">← Back to Articles</a>
        <h1>{{ post['title'] }}</h1>
        <p>By {{ post['author'] }} • {{ post['publish_date'] }} • {{ post['views'] }} views</p>
        {% if post['image_url'] %}
            <img src="{{ post['image_url'] }}" alt="Image" style="max-width: 100%;">
        {% endif %}
        <div>{{ post['content'] }}</div>
    </body>
    </html>
    '''
    return render_template_string(html_template, post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
