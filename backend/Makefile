run:
	@python manage.py runserver 0.0.0.0:8000

migrations:
	@python manage.py makemigrations && python manage.py migrate

super:
	@python manage.py createsuperuser

checklist:
	@python manage.py check --deploy

active:
	@pipenv shell

requirements:
	@pip freeze > requirements.txt

dependencies:
	@pipenv sync

langcheck:
	@pycodestyle *.py

test:
	@pytest shop/tests.py

db:
	@touch db.sqlite3

dummy:
	@python manage.py populate_db
