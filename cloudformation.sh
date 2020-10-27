#!/bin/sh

docker-compose up -d

# Wait a bit for docker to go up
sleep 5


aws cloudformation create-stack \
  --endpoint-url http://localhost:4566 \
  --stack-name mniststack \
  --template-body file://mniststack.yaml \
  --profile localstack


