FROM python:3.13-alpine AS builder
ENV PIPENV_VENV_IN_PROJECT=1
RUN python -m pip install pipenv
RUN mkdir /app
WORKDIR /app
COPY . .
RUN python -m pipenv install


FROM python:3.13-alpine AS runtime
COPY --from=builder /app /app

WORKDIR /app/AllUni/
EXPOSE 8000 
CMD sh -c "../.venv/bin/python manage.py migrate && ../.venv/bin/python manage.py runserver 0.0.0.0:8000"
ENV debug=1
