import os
from flask import Flask, request
import psycopg2
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Общее количество HTTP-запросов",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Время обработки запроса (секунды)",
    ["endpoint"]
)


def get_db_con():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        dbname=os.getenv("DB_NAME", "flask_db"),
        user=os.getenv("DB_USER", "neo"),
        password=os.getenv("DB_PASS", "1111"),
        port=os.getenv("DB_PORT", "5432")
    )
    return connection


@app.before_request
def before_request():
    request._timer = REQUEST_LATENCY.labels(request.path).time()
    request._timer.__enter__()


@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.path).inc()
    if hasattr(request, "_timer"):
        request._timer.__exit__(None, None, None)
    return response


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
    cur.execute("INSERT INTO users (name) VALUES (%s)", (user,))
    conn.commit()
    cur.close()
    conn.close()
    return f"{user} Добавлен"


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


