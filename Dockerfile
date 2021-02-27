FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

WORKDIR /app

COPY ./dnsviz_api/ /app/dnsviz_api

RUN python3 setup.py develop

ENTRYPOINT [ "python3" ]

CMD [ "dnsviz_api/wsgi.py" ]