### Step 1: Create a role in AWS IAM
Go to AWS IAM and create a role.
1. Go to the `roles` page in IAM and click on `Create role` on the right top side.
2. Click `Amazon service` as Trusted entity type and `Lambda` as Use Case, then `next`. 
3. Search and choose policy `AWSLambdaKinesisExecutionRole`, then `Next`. 
4. Name it as `lambda-kinesis-role` then create it.
### Step 2: Create a Lambda function

1. Go to AWS Lambda and create a function as follows.
![lambdafunc.png](..%2Fimages%2Flambdafunc.png)
2. Edit script of Lambda function
   1) Default script:
   ![lambdacode.png](..%2Fimages%2Flambdacode.png)
   2) Test script:
   ![lambdachanges.png](..%2Fimages%2Flambdachanges.png)
   **Note**: `deploy` it everytime makes any changes to the script.

   3) Another example:
   ![lambdafunc2.png](..%2Fimages%2Flambdafunc2.png)
### Step 3: Create Kinesis data stream
1. Go to AWS Kinesis, and create `Kinesis Data Streams` with the name of it as `ride_events` and `provisioned`, then create it. 
2. Go to Lambda and click on `Add triger`. Select `Kinesis` as a resource and find the stream `ride_events`, then `add` it. 
![lambdatrigger.png](..%2Fimages%2Flambdatrigger.png)
### Step 4: Send test event (string) to Lambda.

1. Make sure the script is as below:
    ```
    import json
    def prepare_features(ride):
        features = {}
        features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
        features['trip_distance'] = ride['trip_distance']
        return features
    
    
    def predict(features):
        return 10.0
    
    def lambda_handler(event, context):
        print(json.dumps(event))
        prediction = 10
        ride_id = 123
    
        return {
            'ride_duration': prediction,
            'ride_id': ride_id
        }
    ```
   and `deploy` it.
2. Add new policy to IAM User - `AmazonKinesisFullAccess`
![iamuser.png](..%2Fimages%2Fiamuser.png)
3. Run the following to send a record (`string`) to kinesis. [Simple example](Perform Basic Kinesis Data Stream Operations Using the AWS CLI
)

   ```
   KINESIS_STREAM_INPUT=YOUR_KNISIS_NAME
   aws kinesis put-record \
       --stream-name ${KINESIS_STREAM_INPUT} \
       --partition-key 1 \
       --data "Hello, this is a test."
   ```
   The response should be:
   ![DTKINESS.png](..%2Fimages%2FDTKINESS.png)


4. Go to **Lambda > Monitor > logs > View CloudWatch logs**, copy the `data`
![kinesisKMS.png](..%2Fimages%2FkinesisKMS.png)

5. Re-edit the `configure test evet` with an event test as:
   ```
   {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49642651173544153298181180874739743104392118471204274178",
                "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg==",
                "approximateArrivalTimestamp": 1689436861.63
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49642651173544153298181180874739743104392118471204274178",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::135673905301:role/lambda-kinesis-role",
            "awsRegion": "ca-central-1",
            "eventSourceARN": "arn:aws:kinesis:ca-central-1:135673905301:stream/ride-events"
        }
    ]
   }
   ```
   and get the result:

   ![lambdare.png](..%2Fimages%2Flambdare.png)

### Step 5: Send test event (Json) to Lambda


1. Run the following to send a record (`Json`) to kinesis.
   ```
   aws kinesis put-record \
       --stream-name ${KINESIS_STREAM_INPUT} \
       --partition-key 1 \
       --data '{
           "ride": {
               "PULocationID": 130,
               "DOLocationID": 205,
               "trip_distance": 3.66
           }, 
           "ride_id": 156
       }'
   ```
   ### Note: 
   if the response is "Invalid base64: xxxx", add `--cli-binary-format raw-in-base64-out
\` and resend it again.
![kinesisJson.png](..%2Fimages%2FkinesisJson.png)


2. Re-edit the `configure test evet` with an new event test as: 
   ```
   {
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
   ```
   
### Step 6: Send prediction to another Kinesis stream
1. Edit the script for obtain all the predictions:
```python
import base64
import json


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    return 10.0


def lambda_handler(event, context):
    print(json.dumps(event))

    predictions = []

    for record in event['Records']:
       encoded_data = record['kinesis']['data']
       decoded_data = base64.b64decode(encoded_data).decode('utf-8')
       ride_event = json.loads(decoded_data)

       ride = ride_event['ride']
       ride_id = ride_event['ride_id']

       features = prepare_features(ride)
       prediction = predict(features)

       predictions.append({
          'ride_duration': prediction,
          'ride_id': ride_id
       })

    return {
       'predictions': predictions
    }

```



Since we do not have client architecture and can not send the response to clients directly, it is better to send the response to another stream.
2. Create another data stream.

Name a Kinesis stream as `ride_predictions` the same as STEP 3
3. Script of sending outputs to another stream.
```python
import json
import os
import boto3
import base64
kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_preditions')


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    return 10.0


def lambda_handler(event, context):
    predictions_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)

        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
    
        features = prepare_features(ride)
        prediction = predict(features)
        

        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': '123',
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }
        print(json.dumps(prediction_event))

        kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)
            )
        predictions_events.append(prediction_event)



    return {
        'prediction': predictions_events

    }

```
4. Create a `PutRecord` policy 

Due to `An error occurred (AccessDeniedException) when calling the PutRecord operation: xxxx`, create a Policy for Kinesis of `PutRecord`.
Go to IAM Role, and find the role-`lambda-kinesis-role` we created in previous step. Click on `Add Policy > Create inline Policy`. Under `Select a service`, find and click `Kinesis`. Uner `Access level`, choose `write > PutRecord & PutRecords`.
Add your new Kinesis stream ARN `arn:aws:kinesis:::stream/ride_preditions`. Finally, `Next`. Name your policy as `lambda-kinesis-write-to-ride-predictions`. After create it, add it to your Permissions policies.
5. Run for the result

![OutputStream.png](..%2Fimages%2FOutputStream.png)

6. Write output to ride_predictions kinesis stream.
P.S. I write my output Kinesis stream wrongly in `ride_preditions`
```shell
KINESIS_STREAM_OUTPUT='ride_predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
```
The final result should be: 

![result_kinesis.png](..%2Fimages%2Fresult_kinesis.png)


7. (optional) Try the recall of the responses
```shell
echo $SHARD_ITERATOR
echo $RESULT

```

### STEP 7: Add model to Lambda
1. Create `lambda_function.py` under streaming folder in local environment, then copy the code in Lambda to this python file.
2. Copy the code which is below in `predict-pipline-se.py` to `lambda_function.py`
```
import mlflow 

RUN_ID = os.getenv('RUN_ID')

logged_model = f's3://zoomcamp-mlops/1/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)
 ```

3. Create a [test.py](test.py) file.

4. Edit [lambda_function.py](lambda_function.py), and run

```shell
export PREDICTIONS_STREAM_NAME="ride_predictions"
export RUN_ID="YOUR_RUN_ID"
export TEST_RUN="True"

python test.py
```
![response.png](..%2Fimages%2Fresponse.png)

### STEP 8: Create a docker image
1. Create virtual environment
```bash

pipenv install boto3 mlflow scikit-learn --python=3.9
```
2. Create a docker file
   - Go to [Amazon ECR Public Gallery](https://gallery.ecr.aws/) and find `Lambda/Python > Image Tags > 3.9`. Copy address.





### Notes:
1. If your log data is not base64-encoded, as:
![kinesisKMS.png](..%2Fimages%2FkinesisKMS.png)

   Check [doc](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html#API_PutRecord_ResponseSyntax) here.

   **Problem**: 

   The `EncryptionType` since the encryption type is on `NONE` now, which do not encrypt the records in the stream.
   ![log.png](..%2Fimages%2Flog.png)

   **ANS**: [Solotion](https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/Kinesis/stream-encrypted-with-kms-customer-master-keys.html#:~:text=03%20In%20the%20main%20navigation,available%20in%20the%20Encryption%20section.)

   1) Go to `Kinesis: ride-events`
   ![lambdatrigger.png](..%2Fimages%2Flambdatrigger.png)

   2) Go to ` Configuration > Encryption > Edit`, click on `Enable server-side encryption` and `Use AWS managed CMK`, then `save changes`.

   3) Resend a record to Kinesis, if it says `Invalid base64: xxxx`, add `--cli-binary-format raw-in-base64-out` and resend it again.