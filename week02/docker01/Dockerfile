FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY app.py .

EXPOSE 8080
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
