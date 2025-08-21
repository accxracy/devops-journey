FROM postgres:17

COPY init.sql /docker-entrypoint-initdb.d/


ENV POSTGRES_USER=neo
ENV POSTGRES_PASSWORD=1111
ENV POSTGRES_DB=flask_db

EXPOSE 5432
