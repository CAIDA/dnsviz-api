.PHONY: build run stop all

all: build run

build:
	docker build -t dnsviz-api:latest .

run:
	docker run -d -p 5000:5000 dnsviz-api

stop:
	docker container ls | grep dnsviz-api | awk '{print $$1;}' | xargs docker container stop
