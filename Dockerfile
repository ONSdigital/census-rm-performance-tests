FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv && pipenv install --deploy --system

COPY tests/* tests/

EXPOSE 8089

ENTRYPOINT [ "locust", "-f", "tests/casesvc_locustfile.py" ]

# Default to displaying Locust's help if no --host= option passed at runtime.
CMD ["-h"]
