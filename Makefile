.PHONY: install clean database build build-docker test lint

install:
	npm install
	npm run build
	python3 -m pip install -r requirements.txt

clean:
	rm -rf ./backend/ticketvise/migrations || true
	rm ./backend/db.sqlite3 || true
	rm ./backend/ticketvise/static/*.js || true
	rm ./backend/ticketvise/static/*.css || true
	rm ./backend/ticketvise/static/*.map || true

build:
	python3 ./backend/manage.py makemigrations ticketvise
	python3 ./backend/manage.py migrate
	python3 ./backend/manage.py collectstatic --no-input
	npm run watch

build-demo: clean build
	python3 ./backend/manage.py generate_database

build-docker:
	docker-compose up -d --build

test:
	docker-compose exec -T web python manage.py test tests/ --parallel --failfast --no-input
	npm test

lint:
	flake8 ./ --max-line-length 120

start:
	docker-compose up --build

stop:
	docker-compose down -v --remove-orphans
