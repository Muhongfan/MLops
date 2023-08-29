import sys
sys.path.append("..")
import  lambda_function


import requests
import json
import logging

from deepdiff import DeepDiff


logging.getLogger("mlflow").setLevel(logging.DEBUG)
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
# response = requests.post(url, json=event)
# print("Hello Piggy")
# print(response.text)
# print("Hello Puppy")
actual_response = lambda_function.lambda_handler(event, None)
print('acutual response')

print(json.dumps(actual_response, indent=2))

expected_response= {
        'predictions': [
            {
                'model': 'ride_duration_prediction_model',
                'version': '7c8bb75fadea44aa9337ec3de35c430e',
                'prediction': {
                    'ride_duration': 18.2,
                    'ride_id': 156,
                },
            }
        ]
    }
diff = DeepDiff(actual_response, expected_response, significant_digits =1)
print(f'diff={diff}')
# diff={'values_changed': {"root['predictions'][0]['prediction']['ride_duration']": {'new_value': 18.1, 'old_value': 18.168945726405326}}}

assert 'type_changes' not in diff
assert 'values_changed' not in diff
#diff={}
# assert actual_response == expected_response