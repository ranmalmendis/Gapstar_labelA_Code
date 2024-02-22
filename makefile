start_from_begining: migrate insert_test_data run

insert_test_data:
	python3 manage.py insert_sample_data

migrate:
	python3 manage.py makemigrations 
	python3 manage.py migrate

run:
	python3 manage.py runserver

build:
	docker build -t autocompany .

docker_run:
	docker run -p 8000:8000 -d autocompany


