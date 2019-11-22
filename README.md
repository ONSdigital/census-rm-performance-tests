# Census Response Management Performance Tests
Behave performance tests for Census Response management.

## Sample files
This test is designed to run a performance test against a representative sample file with all treatment codes. Three dummy [sample files](/resources/sample_files) of various sizes have 
already been generated in the repo.

## Run locally
You can run the tests locally against the [census-rm-docker-dev](https://github.com/ONSdigital/census-rm-docker-dev) services but note that these may have issues with the full sample depending on your docker resource allocation.

Install dependencies (requires [pipenv](https://docs.pipenv.org/en/latest/)) with `make install`.

Run the tests with `make performance-test`.
The default sample file has 1 row per treatment code so it can be run through quickly. You can change the target sample file with the `SAMPLE_FILE_PATH` environment variable e.g
`SAMPLE_FILE_PATH=sample.csv make performance-test`

You can also alter the action rule delay (to allow longer for ingestion of large samples) with `ACTION_RULE_DELAY_MINUTES` and the print file production time limit with `PRINT_FILE_TIME_LIMIT_MINUTES`.

## Run tests against in GCP project

Run the [`run_gke.sh`](run_gke.sh) bash script with the environment variables (defined in [the table below](#script-environment-variables)).

### Examples

NB: assumes infrastructure and services exist in respective projects.

To run the performance tests (`latest` image in GCR) in a pod in census-rm-ci:
```bash
./run_gke.sh
```
To run a locally-modified version of the performance tests in a pod in a dev GCP project (builds and pushes the docker image to the project's GCR):
```bash
BUILD=true ENV=test-env ./run_gke.sh
```
To run the performance tests using the `latest` image from the census-rm-ci GCR in a pod in a dev GCP project (otherwise defaults to the image in the project's GCR):
```bash
IMAGE=ci ENV=test-env ./run_gke.sh
```
Build and push a locally-modified version of the performance tests and then run in a pod in another dev GCP project:
```bash
BUILD=true IMAGE="eu.gcr.io/census-rm-at/rm/census-rm-performance-tests:latest" ENV=test-env ./run_gke.sh
```

You can alter the environment variables to use different sample files and timings by editing the [kubernetes.env](kubernetes.env)

### Script Environment variables

| Name        | Description                                                                                                                                                                         | Example                                                                      | Default                                                          | Required |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- | -------- |
| `ENV`       | The environment to run the tests in and against, it will try to use an existing project of the form `census-rm-<ENV>`. If not present, the script will use the current k8s context. | `ENV=test-env`                                                               | None                                                             | no       |
| `IMAGE`     | The path to the performance tests Docker image to use in the k8s pod (lazy option `ci` to use the default master image).                                                            | `IMAGE="eu.gcr.io/census-rm-test-env/rm/census-rm-performance-tests:latest"` | `eu.gcr.io/census-rm-$ENV/rm/census-rm-performance-tests:latest` | no       |
| `BUILD`     | A boolean (`true` or not set string) to toggle the build and push of the performance tests as a Docker image.                                                                       | `IMAGE=true`                                                                 | None                                                             | no       |
| `NAMESPACE` | The k8s namespace to run the performance tests as a pod in.                                                                                                                         | `NAMESPACE=rm`                                                               | None                                                             | no       |

### Run RabbitMQ Performance testing

Run
```bash
make rabbitmq-perf-tool
docker push eu.gcr.io/census-rm-ci/rm/census-rm-rabbit-performance
```
Set Kubectl to census-rm-performance and then apply the deployment
```bash
gcloud beta container clusters get-credentials rm-k8s-cluster --region <REGION> --project <PERFORMANCE_PROJECT_NAME>
kubectl apply -f rabbit-perf-test/census-rm-rabbit-perf-deployment.yml
```

Shell into pod to run a basic test
```bash
./basic-test.sh
```

For documentation on running tests:

https://rabbitmq.github.io/rabbitmq-perf-test/stable/htmlsingle/#using-environment-variables-as-options

Running a bench mark test:
```bash
bin/runjava com.rabbitmq.perf.PerfTestMulti publish-consume-spec.js publish-consume-result.js 
```
For documentation on benchmarking see:
https://github.com/rabbitmq/rabbitmq-perf-test/blob/master/html/README.md


## Copyright
Copyright (c) 2018 Crown Copyright (Office for National Statistics)
