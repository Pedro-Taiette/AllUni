FROM python:3.13-alpine AS builder
ENV PIPENV_VENV_IN_PROJECT=1
RUN python -m pip install pipenv
RUN mkdir /app
WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN python -m pipenv install

COPY AllUni AllUni/
COPY README.md LICENSE ./

FROM python:3.13-alpine AS runtime
COPY --from=builder /app /app

WORKDIR /app/AllUni/

ENV SQLITE_DB_PATH=/app/data/db.sqlite3
ENV DEBUG=1

VOLUME /app/data

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /app/data && touch $SQLITE_DB_PATH && chmod 777 $SQLITE_DB_PATH && ../.venv/bin/python manage.py migrate && ../.venv/bin/python manage.py runserver 0.0.0.0:8000"]
