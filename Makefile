build:
	@docker-compose up --build

tests:
	@docker-compose run backend python manage.py test

stop:
	@docker-compose down