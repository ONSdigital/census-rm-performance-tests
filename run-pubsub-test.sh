kubectl delete pod performance-tests
kubectl run performance-tests -it --command --rm --quiet \
  --image=eu.gcr.io/census-rm-ci/census-rm-performance-tests:adamhawtin-pubsub \
  --restart=Never \
  $(while read env; do echo --env=${env}; done <kubernetes.env) \
  --env=SFTP_HOST=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.host}" | base64 --decode) \
  --env=SFTP_USERNAME=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.username}" | base64 --decode) \
  --env=SFTP_KEY=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.private-key}") \
  --env=SFTP_PASSPHRASE=$(kubectl get secret sftp-ssh-credentials -o=jsonpath="{.data.passphrase}" | base64 --decode) \
  --env=SFTP_PPO_DIRECTORY=$(kubectl get configmap project-config -o=jsonpath="{.data.sftp-ppo-supplier-directory}") \
  --env=SFTP_QM_DIRECTORY=$(kubectl get configmap project-config -o=jsonpath="{.data.sftp-qm-supplier-directory}") \
  --env=RABBITMQ_USER=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-username}" | base64 --decode) \
  --env=RABBITMQ_PASSWORD=$(kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-password}" | base64 --decode) \
  --env=RABBITMQ_MAN_PORT=15672 \
  --env=GOOGLE_SERVICE_ACCOUNT_JSON=$(kubectl get secret pubsub-credentials -o=jsonpath="{.data['service-account-key\.json']}") \
  --env=GOOGLE_APPLICATION_CREDENTIALS="/home/performancetests/service-account-key.json" \
  --env=PUBSUB_PROJECT="census-rm-$ENV" \
  --env=PUBSUB_TOPIC="receipting-topic-$ENV" \
  --env=PUBSUB_TEST_QUANTITY=$PUBSUB_TEST_QUANTITY \
  -- /bin/bash -c "sleep 2; behave pubsub_features --tags=@pubsub --no-capture --no-logcapture"
