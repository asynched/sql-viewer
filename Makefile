install:
	python -m pip install -r requirements.txt

dev:
	python main.py

run:
	gunicorn main:app
