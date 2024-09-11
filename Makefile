build:
	@docker-compose up --build

tests:
	@docker-compose run backend make test

stop:
	@docker-compose down