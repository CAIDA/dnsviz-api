FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

WORKDIR /app

COPY ./dnsviz_api/ /app/dnsviz_api

RUN pip3 install --no-cache-dir -e .

EXPOSE 5000

WORKDIR /app/dnsviz_api

CMD gunicorn --worker-class gevent --workers 3 --bind 0.0.0.0:5000 wsgi:app --worker-connections 1000 --timeout 5 --keep-alive 5 --log-level info