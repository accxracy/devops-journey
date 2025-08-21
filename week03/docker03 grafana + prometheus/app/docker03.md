# Мониторинг Flask-приложения с Prometheus и Grafana

Это дополнение к прошлому пайплайну: [devops-journey/week03/docker02 (compose), best practice](https://github.com/accxracy/devops-journey/tree/main/week03/docker02%20(compose)%2C%20best%20practice)

Здесь мы добавляем мониторинг приложения с помощью **Prometheus** и **Grafana**.


## Структура проекта:
```
app/
    backend/
        Dockerfile
        main.py
    database/
        init.sql
        Dockerfile
    prometheus/
        prometheus.yml
        
    docker-compose.yml
```


---

## 1. Интеграция Prometheus в Flask

Добавляем следующие строки для сбора метрик:

```python
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

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

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
```

---

## 2. Вынос зависимостей в отдельный файл

Для удобства создаём файл зависимостей:

```bash
pip freeze > req.txt
```

---

## 3. Модификация Dockerfile для бекенда

```dockerfile
FROM python:3.13-alpine AS build

WORKDIR /app

COPY . .

RUN pip install -r req.txt

FROM python:3.13-alpine

RUN adduser -S flask -u 1001

WORKDIR /app

COPY --from=build --chown=flask:flask /app /app

USER flask

CMD ["python", "main.py"]
```

---

## 4. Dockerfile для БД и init.sql

Никак не изменяем.

---

## 5. Prometheus конфигурация

В каталоге `prometheus` создаём файл `prometheus.yml`:

```yaml
global:
    scrape_interval: 5s

scrape_configs:
    - job_name: 'flask'
      static_configs:
          - targets: ['flask_app:5000']
```

---

## 6. Docker-compose

Добавляем сервисы Prometheus и Grafana, меппим порты:

```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: prometheus
  volumes:
    - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"
  depends_on:
    - "prometheus"
```

---

## 7. Поднимаем контейнеры

```bash
docker-compose up --build
```

---

## 8. Grafana

Переходим по адресу [http://localhost:3000/](http://localhost:3000/).  

Добавляем новый источник данных (**Prometheus**). В `URL` указываем:

```
http://prometheus:9090/
```

---

## 9. Дашборд

Добавляем визуализацию метрик в дашборд Grafana.

---

На этом базовая настройка мониторинга для веб-приложения завершена.

