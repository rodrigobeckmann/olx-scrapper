routine:
	docker compose exec web python manage.py scrap_data

build:
	docker compose build

run:
	docker compose up -d

make-migrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

shell:
	docker compose exec web python manage.py shell