install:
	python -m pip install -r requirements.txt

run:
	waitress-serve --host=127.0.0.1 --port=8081 main:app
