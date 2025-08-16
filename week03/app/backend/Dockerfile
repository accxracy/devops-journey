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
