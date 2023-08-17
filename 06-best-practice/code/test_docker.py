import requests
import lambda_function
import json

event = {

    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49642651173544153298181181325149235718214587400895594498",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDE1NgogICAgfQ==",
                "approximateArrivalTimestamp": 1689437986.135
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49642651173544153298181181325149235718214587400895594498",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::135673905301:role/lambda-kinesis-role",
            "awsRegion": "ca-central-1",
            "eventSourceARN": "arn:aws:kinesis:ca-central-1:135673905301:stream/ride-events"
        }
    ]

}

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(url, json=event)
print(response.json())
# result = lambda_function.lambda_handler(event, None)
# print(result)