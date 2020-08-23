.PHONY: install clean database build build-docker test lint

install:
	npm install
	npm run build
	python3 -m pip install -r requirements.txt

clean:
	rm -rf ./backend/ticketvise/migrations || true
	rm ./backend/ticketvise.sqlite3 || true
	rm ./backend/ticketvise/static/*.js || true
	rm ./backend/ticketvise/static/*.css || true
	rm ./backend/ticketvise/static/*.map || true

build:
	cd ./backend/ && python3 manage.py migrate
	cd ./backend/ && python3 manage.py collectstatic --no-input
	npm run watch

build-demo: clean
	cd ./backend/ && python3 manage.py migrate
	cd ./backend/ && python3 manage.py collectstatic --no-input
	cd ./backend/ && python3 manage.py insert_demo_data
	npm run watch

build-docker:
	docker-compose up -d --build

test:
	docker-compose exec -T web python manage.py test ticketvise/tests/ --parallel --failfast --no-input
	npm test

lint:
	flake8 ./ --max-line-length 120

start:
	docker-compose up --build

stop:
	docker-compose down -v --remove-orphans
