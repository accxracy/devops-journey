from flask import Flask
import psycopg2


app = Flask(__name__)

def get_db_con():
    connection = psycopg2.connect(
        host='database',
        dbname='flask_db',
        user='neo',
        password='1111',
        port='5432'
    )
    return connection


@app.route('/')
def index():
    conn = get_db_con()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return f"{' '.join([user[1] for user in users])}"


@app.route('/add/<user>')
def add(user):
    conn = get_db_con()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (user, ))
    conn.commit()
    cur.close()
    conn.close()

    return f"{user} Добавлен"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

