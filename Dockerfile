FROM python:3.7-slim

RUN pip install pipenv

RUN apt-get update -y && apt-get install -y python-pip curl git && groupadd --gid 1000 performancetests && \
    useradd --create-home --system --uid 1000 --gid performancetests performancetests
WORKDIR /home/performancetests

COPY Pipfile* /home/performancetests/
RUN pipenv install --deploy --system
USER performancetests

COPY --chown=performancetests . /home/performancetests