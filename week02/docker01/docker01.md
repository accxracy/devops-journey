# Контейнеризация простейшего Flask-приложения

Этот пример демонстрирует, как контейнеризировать минимальное Flask-приложение с помощью Docker.

## 📦 Установка зависимостей

Установим `flask` (если он ещё не установлен):

```bash
pip install flask
```

## 📝 Создание приложения

Создаем файл `app.py` со следующим содержанием:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Index page"

if __name__ == "__main__":
    app.run()
```

## 📄 Создание `requirements.txt`

Для управления зависимостями и удобства масштабирования создайте файл `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## 🐳 Dockerfile

Создаем `Dockerfile` в той же директории:

```Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8080

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8080"]
```

### Объяснение ключевых строк:

- `FROM python:3.13-slim` — минимальный базовый образ Python
- `WORKDIR /app` — рабочая директория внутри контейнера
- `COPY` — копируем зависимости и приложение
- `RUN pip install` — устанавливаем зависимости
- `EXPOSE 8080` — открываем порт 8080
- `ENTRYPOINT` — запускаем сервер Flask

## 🛠️ Сборка образа

Выполняем команду в терминале из каталога с Dockerfile:

```bash
docker build -t flask_image .
```

- `-t flask_image` — задаёт имя образу
- `.` — путь к текущей директории, где находится Dockerfile

## ▶️ Запуск контейнера

```bash
docker run -p 8080:8080 flask_image
```

- `-p 8080:8080` — пробрасываем порт
- `flask_image` — имя образа

## 🌐 Результат

Откройте в браузере: [http://localhost:8080](http://localhost:8080)

Вы должны увидеть сообщение **Index page**.

---
