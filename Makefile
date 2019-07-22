performance-test:
	pipenv run behave --no-capture

install:
	pipenv install --dev

lint:
	pipenv run flake8

check:
	pipenv check

test: lint check performance-test
