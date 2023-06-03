setup:
	cp .env.sample .env
build:
	docker-compose build
up:
	docker-compose up