#!/usr/bin/env bash

set -e

if [ -z "$ENV" ]; then
    echo "No ENV set. Using kubectl current context."
    if [ -z "$IMAGE" ] || [ "$IMAGE" = "ci" ]; then
        IMAGE=eu.gcr.io/census-rm-ci/rm/census-rm-performance-tests:latest
    fi
else
    GCP_PROJECT=census-rm-$ENV
    if [ -z "$IMAGE" ]; then
        IMAGE=eu.gcr.io/$GCP_PROJECT/rm/census-rm-performance-tests:latest
    elif [ "$IMAGE" = "ci" ]; then
        IMAGE=eu.gcr.io/census-rm-ci/rm/census-rm-performance-tests:latest
    fi

    gcloud config set project $GCP_PROJECT
    gcloud container clusters get-credentials rm-k8s-cluster \
        --region europe-west2 \
        --project $GCP_PROJECT
fi

#if [ "$BUILD" = "true" ]; then
#    echo "Building and pushing Docker image [$IMAGE]..."
#    read -p "Are you sure (y/N)? " -n 1 -r
#    if [[ $REPLY =~ ^[Yy]$ ]]; then
#        docker build -t $IMAGE .
#        docker push $IMAGE
#    else
#        exit 1
#    fi
#fi

docker build -t $IMAGE .
docker push $IMAGE

echo "Using RM Performance Tests image [$IMAGE]."
if [ "$NAMESPACE" ]; then
    kubectl config set-context $(kubectl config current-context) --namespace=$NAMESPACE
    echo "Set kubectl namespace for subsequent commands [$NAMESPACE]."
fi
echo "Running Census RM Performance Tests [`kubectl config current-context`]..."


kubectl run performance-tests -it --command --rm --quiet --generator=run-pod/v1 \
    --image=$IMAGE --restart=Never \
    $(while read env; do echo --env=${env}; done < kubernetes.env) \
    --env=SFTP_HOST=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.host}" | base64 --decode) \
    --env=SFTP_USERNAME=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.username}" | base64 --decode) \
    --env=SFTP_KEY=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.private-key}") \
    --env=SFTP_PASSPHRASE=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.passphrase}" | base64 --decode) \
    --env=SFTP_PPO_DIRECTORY=$(kubectl get configmap project-config -o=jsonpath="{.data.sftp-ppo-supplier-directory}") \
    --env=SFTP_QM_DIRECTORY=$(kubectl get configmap project-config -o=jsonpath="{.data.sftp-qm-supplier-directory}") \
    --env=RABBITMQ_USER=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-username}" | base64 --decode) \
    --env=RABBITMQ_PASSWORD=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-password}" | base64 --decode) \
    --env=RABBITMQ_MAN_PORT=15672 \
    --env=SAMPLE_FILE_PATH=resources/sample_files/1_per_treatment_code.csv \
    -- /bin/bash -c "sleep 2; behave --no-capture"
