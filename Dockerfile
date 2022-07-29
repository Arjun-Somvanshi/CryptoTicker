FROM python:3.10

WORKDIR /code

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
COPY .env /code/.env

RUN pip install pipenv
RUN pipenv install  

COPY ./app /code/app

CMD ["pipenv", "run", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]
