FROM python:3.7-alpine

MAINTAINER "Benedicte Emilie Brækken <b@brkn.io>"

RUN apk add \
    postgresql-dev \
    gcc \
    musl-dev \
  && pip install pipenv

WORKDIR /app

COPY Pipfile* /app/

RUN pipenv install

COPY app.py /app/
COPY work_timer_back /app/work_timer_back

ENV FLASK_ENV=production
ENV FLASK_APP=app.py
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=80

EXPOSE 80/tcp

CMD [ "pipenv", "run", "python", "./app.py" ]
