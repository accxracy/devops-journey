
# Пример сборки приложения с backend (Flask) и PostgreSQL в контейнерах через docker-compose

## Структура проекта:
```
app/
    backend/
        Dockerfile
        main.py
    database/
        init.sql
        Dockerfile
    docker-compose.yml
```

---

### 1. Установка зависимостей
```bash
pip install Flask psycopg2-binary
```

---

### 2. Создание базы данных и таблицы (`init.sql`)
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO users (name) VALUES ('Alex'), ('John');
```

---

### 3. Flask-приложение (`main.py`)
```python
import os
from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_con():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        dbname=os.getenv("DB_NAME", "flask_db"),
        user=os.getenv("DB_USER", "neo"),
        password=os.getenv("DB_PASS", "1111"),
        port=os.getenv("DB_PORT", "5432")
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
```

---

### 4. Настройки подключения через переменные окружения
```python
host=os.getenv("DB_HOST", "database"),
dbname=os.getenv("DB_NAME", "flask_db"),
user=os.getenv("DB_USER", "neo"),
password=os.getenv("DB_PASS", "1111"),
port=os.getenv("DB_PORT", "5432")
```

---

### 5. Создание сети Docker (опционально)
```bash
docker network create app-network
```

---

### 6. Dockerfile для backend
```dockerfile
FROM python:3.13.7-alpine AS build

WORKDIR /app

COPY main.py ./

RUN pip install Flask psycopg2-binary -t /app

FROM python:3.13.7-alpine

RUN adduser -S flask -u 1001

WORKDIR /app

COPY --from=build --chown=flask:flask /app /app

USER flask

CMD ["python", "main.py"]
```

---

### 7. Dockerfile для базы данных
```dockerfile
FROM postgres:17

COPY init.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER=neo
ENV POSTGRES_PASSWORD=1111
ENV POSTGRES_DB=flask_db

EXPOSE 5432
```

---

### 8. Проверка работы вручную

#### 8.1 Сборка контейнеров
```bash
cd backend
docker build -t backend .

cd ../database
docker build -t database .
```

#### 8.2 Запуск контейнеров
```bash
docker run -d --name database --network app-network -p 5432:5432 database
docker run -d --name backend --network app-network -p 5000:5000 backend
```

#### 8.3 Проверка результата
Открываем [http://localhost:5000/](http://localhost:5000/) и видим данные из таблицы.

---

### 9. docker-compose.yml
```yaml
services:
  database:
    build:
      context: ./database
    container_name: database
    environment:
      POSTGRES_USER: neo
      POSTGRES_PASSWORD: 1111
      POSTGRES_DB: flask_db
    ports:
      - "5432:5432"
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped

  backend:
    build:
      context: ./backend
    container_name: backend
    ports:
      - "5000:5000"
    networks:
      - app-network
    environment:
      - DB_HOST=database
      - DB_NAME=flask_db
      - DB_USER=neo
      - DB_PASS=1111
      - DB_PORT=5432
    depends_on:
      - database

networks:
  app-network:
```

---

✅ Всё готово!
