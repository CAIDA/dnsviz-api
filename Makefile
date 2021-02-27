build:
	docker build -t dnsviz-api:latest .

run:
	docker run -d -p 5000:5000 dnsviz-api

clean:
	rm -rf *__pycache__
