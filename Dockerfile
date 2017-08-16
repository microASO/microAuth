FROM python:2.7-slim

RUN pip install gunicorn json-logging-py flask

COPY logging.conf /logging.conf
COPY gunicorn.conf /gunicorn.conf

COPY ./python/ /

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":8000", "myapp:app"]
