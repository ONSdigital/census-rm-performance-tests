cat  << EOF
[{'name': 'consume', 'type': 'simple', 'uri': 'amqp://$RABBITMQ_USER:$RABBITMQ_PASSWORD@rabbitmq-discovery.default.svc.cluster.local', 'params':
[{'time-limit': 30, 'producer-count': 4, 'consumer-count': 2}]}]
EOF
