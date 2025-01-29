FROM python:3.12

RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
COPY pyproject.toml $APP_HOME
COPY poetry.lock $APP_HOME
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
RUN python -m venv .venv
RUN poetry install --without dev

# copy project
COPY . $APP_HOME

# create the additional directories
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/media

COPY ./start .
RUN sed -i 's/\r$//g' start
RUN ["chmod", "+x", "start"]
