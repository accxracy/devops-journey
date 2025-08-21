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

