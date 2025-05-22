FROM python:3.13-alpine

RUN python -m pip install pipenv
RUN mkdir /app
WORKDIR /app
COPY . .
RUN python -m pipenv install


WORKDIR /app/AllUni/
EXPOSE 8000 
CMD sh -c "pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8000"
ENV debug=1
