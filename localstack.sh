#!/bin/sh

docker-compose up -d

# Wait a bit for docker to go up
sleep 5

# Create S3 Buckets
aws --endpoint-url=http://localhost:4566 s3 mb s3://data
aws --endpoint-url=http://localhost:4566 s3 mb s3://models

# Sync local directories with localstack S3
aws --endpoint-url=http://localhost:4566 s3 sync data/mnist s3://data/mnistq

# Create Dynamo Tables
#aws --endpoint-url=http://localhost:4569 dynamodb create-table --table-name SolarForecastResultsTable  --attribute-definitions AttributeName=regionCode,AttributeType=S AttributeName=time_period,AttributeType=N --key-schema AttributeName=regionCode,KeyType=HASH AttributeName=time_period,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=500,WriteCapacityUnits=500
#aws --endpoint-url=http://localhost:4569 dynamodb create-table --table-name WindForecastResultsTable  --attribute-definitions AttributeName=regionCode,AttributeType=S AttributeName=time_period,AttributeType=N --key-schema AttributeName=regionCode,KeyType=HASH AttributeName=time_period,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=500,WriteCapacityUnits=500
#aws --endpoint-url=http://localhost:4569 dynamodb create-table --table-name AggregationTable  --attribute-definitions AttributeName=regionCode,AttributeType=S AttributeName=timePeriod,AttributeType=N --key-schema AttributeName=regionCode,KeyType=HASH AttributeName=timePeriod,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=500,WriteCapacityUnits=500



