# Census Response Management Performance Tests
[Locust](https://locust.io/) tests for load testing Response Management.

## Running
### Case Service
To run the Locust tasks for the Case service, use:

    docker run -p 8089:8089 -e CASE_ID=<CASE_ID> eu.gcr.io/census-rm-jt-dev/rm-locust --host=<CASE_HOST>

&mdash;Whereby `CASE_ID` is the UUID of a valid case and `CASE_HOST` is the URL of the Case service host.

## Copyright
Copyright (c) 2018 Crown Copyright (Office for National Statistics)