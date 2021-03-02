.PHONY: build run stop all

all: stop build run

build:
	docker build -t dnsviz-api:latest .

run:
	docker run -d -p 5000:5000 dnsviz-api

stop:
	docker container ls | grep dnsviz-api | awk '{print $$1;}' | xargs docker container stop

freeze:
	pip3 freeze --exclude-editable > requirements.txt

deploy:
	docker build -t gcr.io/dnsviz-api/dnsviz-api:latest .
	docker push gcr.io/dnsviz-api/dnsviz-api:latest
