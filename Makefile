performance-test:
	pipenv run behave --no-capture

install:
	pipenv install --dev

lint:
	pipenv run flake8

check:
	# TODO reinstate this once https://github.com/pypa/pipenv/issues/4188 is resolved
	#pipenv check

test: lint check performance-test

build:
	docker build -t eu.gcr.io/census-rm-ci/census-rm-performance-tests .

rabbitmq-perf-test:
	docker build -t eu.gcr.io/census-rm-ci/rm/census-rm-rabbit-performance rabbit-perf-test
