USERNAME=kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-username}" | base64 --decode
PASSWORD=kubectl get secret rabbitmq -o=jsonpath="{.data.rabbitmq-password}" | base64 --decode
cat  << EOF
[{'name': 'consume', 'type': 'simple', 'uri': 'amqp://$USERNAME:$PASSWORD@rabbitmq-discovery.default.svc.cluster.local', 'params':
[{'time-limit': 30, 'producer-count': 4, 'consumer-count': 2}]}]
EOF
