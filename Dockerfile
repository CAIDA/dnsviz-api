FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

WORKDIR /app

COPY ./dnsviz_api/ /app/dnsviz_api

RUN python3 setup.py develop

RUN pip3 install gunicorn[gevent]

EXPOSE 5000

WORKDIR /app/dnsviz_api

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info