
## 01/02
1. Github - Token for identification

**Step 1:** Go to github `Setting->Developer setting->Personal access tokens (classic)->Generate new token(classic)` (**Note:** Make sure to copy your personal access token now. You won’t be able to see it again!)

With your token, connect your remote.

```sh
ssh mlops(replace it with yours)
```

```sh
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages
sudo apt update
sudo apt install gh
```

```sh
gh auth login
```
Follow the questions and finally paste your tokens as required.

**Note:** If you change to another computer, you have to regenerate a new token and `gh auth login` again 


---------------
## 03-orchestration

1. **FileNotFoundError: [Errno 2] No such file or directory**

 ***ANS***: Check the access of S3 block if it is public or not

---------------

## 04-deployment
### Webservice:
1. ERROR: ' Unable to locate credentials. You can configure credentials by running `aws configure`. '
    ![awsconfig.png](imgs%2Fawsconfig.png)

     1). Check configure list if the credential is already set, `aws configure list`
     2). (optional) If it does not, and shows as follows, set the `config` file.
      - AWS Access Key ID [None]: The access key id from IAM 
      - AWS Secret Access Key [None]: The Secret key id from IAM
      - default region name should be the similar format as: `ca-central-1`

2.  `aws s3 ls <target> --recursive` shows the history of all uploaded files

If an error reported as "MlflowException: API request to endpoint /api/2.0/mlflow/experiments/get-by-name failed with error code 403 != 200. Response body: ''", it is because mlflow did not start.


3.  "OSError: [Errno 30] Read-only file system: 'dict_vectorizer.bin'"
ANS: Run `jupyter notebook`, and run it online.


4. HTTPError: HTTP Error 403: Forbidden when call apply_model() in score.ipynb

**Solution**: instead of input_file = f'https://s3.amazonaws.com/nyc-tlc/trip+data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'  use input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'

5. When creating prefect storage, error: ```sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: block_spec
[SQL: ALTER TABLE block_spec RENAME TO block_schema]
(Background on this error at: https://sqlalche.me/e/14/e3q8)```

**Solution**:
```
pipenv run pip install SQLAlchemy==1.4.49 
rm ~/.prefect/orion.db
pipenv shell        
prefect orion database reset -y 
prefect orion start  

```


### Streaming

1. If your log data is not base64-encoded, as:
![kinesisKMS.png](..%2Fimages%2FkinesisKMS.png)

   **Problem**: 

   The `EncryptionType` since the encryption type is on `NONE` now, which do not encrypt the records in the stream.
   ![log.png](..%2Fimages%2Flog.png)

   **ANS**: Check [doc](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html#API_PutRecord_ResponseSyntax) here. 

   [Solotion](https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/Kinesis/stream-encrypted-with-kms-customer-master-keys.html#:~:text=03%20In%20the%20main%20navigation,available%20in%20the%20Encryption%20section.)

   1) Go to `Kinesis: ride-events`
   ![lambdatrigger.png](..%2Fimages%2Flambdatrigger.png)

   2) Go to ` Configuration > Encryption > Edit`, click on `Enable server-side encryption` and `Use AWS managed CMK`, then `save changes`.

   3) Resend a record to Kinesis, if it says `Invalid base64: xxxx`, add `--cli-binary-format raw-in-base64-out` and resend it again.
2. Kinesis does not be connected.:
    ![json.png](..%2Fimages%2Fjson.png)
    
    **ANS**: This is because the Kinesis ('ride-event') is enabled for trigger of lambda. Try to reconnect it.
3. `An error occurred (AccessDeniedException) when calling the CreateRepository operation: User: arn:aws:iam::135673905301:user/mlops-zoom-user is not authorized to perform: ecr:CreateRepository on resource: arn:aws:ecr:ca-central-1:135673905301:repository/duration-model because no identity-based policy allows the ecr:CreateRepository action`

   **ANS**: Go to IAM User policy and add `AmazonEC2ContainerRegistryFullAccess`

4. `No Basic Auth Credentials` Error

    **ANS**: `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com` and then re-run the `docker run`
5. Invalid base64 
    ``` "{
           "ride": {
               "PULocationID": 130,
               "DOLocationID": 205,
               "trip_distance": 3.66
           }, 
           "ride_id": 256
       }"
    ``` 
   when put a new record to the trigger kinesis stream in Step 9.

    **ANS**: Change to add `--cli-binary-format raw-in-base64-out \` in the shell code

5. `An error occurred (ResourceNotFoundException) when calling the GetShardIterator operation: Shard shardId-000000000000 in stream ride_predictions under account 135673905301 does not exist`

   **ANS**: 

   - Verify the Kinesis Data Stream Name: Double-check that the stream name specified in the Lambda function is correct. Ensure that there are no typos or spelling errors in the stream name.

   - Check Kinesis Data Stream Existence: Confirm that the Kinesis data stream "ride_predictions" exists under the AWS account with the ID "135673905301." You can do this by logging in to the AWS Management Console, navigating to the Kinesis service, and checking the list of streams for the specified AWS account.

   - Verify the Shard ID: If you are manually specifying the shard ID in your Lambda function, ensure that you are using the correct shard ID for the "ride_predictions" stream. Shard IDs are unique identifiers for individual shards in a Kinesis data stream.

   - Check Lambda Function Permissions: Ensure that the Lambda function has the necessary permissions to interact with the Kinesis data stream. The Lambda function's execution role should have appropriate permissions (e.g., kinesis:DescribeStream, kinesis:GetShardIterator) to interact with the specified Kinesis stream.

   - Check AWS Region: Make sure that both the Lambda function and the Kinesis data stream are in the same AWS region. Cross-region operations might not be allowed if not explicitly configured.

   - Confirm the Code Logic: Review the Lambda function's code to ensure that the GetShardIterator operation is being called correctly. Double-check that there are no logical errors causing the issue.

   - Look for Recent Changes: If the error started occurring after a recent update or deployment, consider rolling back changes to isolate the cause.

   - CloudWatch Logs: Enable logging for the Lambda function and check the CloudWatch logs to get more details about the error. This might provide additional insights into the issue.



---------------
## 05-monitoring
1. `grafana_1 | Error: ✗ Datasource provisioning error: read /etc/grafana/provisioning/datasources/datasource.yaml: is a directory`

**Solutions**: `docker-compose rm` then restart it with `docker-compose up --build`

2. `OSError: [Errno 30] Read-only file system: './data'` since can not find the relative path 

**Solutions**:
- Change path './data' to absolute address
- Or change the config file of jupyter notebook 
    ```
    jupyter notebook --generate-config 
    cd /Users/amberm (YOUR_USER_NAME)/.jupyter
    vim jupyter_notebook_config.py
    ```
   and then change the default path to the one under your path
   ```
   ## The directory to use for notebooks and kernels
   #  Default: ''
   c.NotebookApp.notebook_dir = 'YOUR_PRO_PATH'
  ``` 
  
3. Install evidently package

**Solutions**:
`conda install -c conda-forge evidently`



---------------

## 06-best-practice 
1. `ModuleNotFoundError: No module named 'model'` when run `model_test.py`
    ***ANS***: Insert into `model_test.py`
    ```
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ```
2. `binascii.Error: Incorrect padding`
    ***ANS***: Change the input `"ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDE1NgogICAgfQ"` to `"ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDE1NgogICAgfQ=="`

3. Info of AWS S3
Check `Run_id` of the models in S3: ` aws s3 ls s3://{YOUR_S3_BUCKET}/1/`
Check `models` of the models in S3: `aws s3 ls s3://zoomcamp-mlops/1/7c8bb75fadea44aa9337ec3de35c430e/artifacts/model/`
Download `models` from S3 to `./model` folder: `aws s3 cp --recursive s3://zoomcamp-mlops/1/7c8bb75fadea44aa9337ec3de35c430e/artifacts/model/ model`

4. Check the info of files in `model` folder: `ls -lh model/`

5. `mlflow.exceptions.MlflowException: The following failures occurred while downloading one or more artifacts from s3://zoomcamp-mlops/1/None/artifacts: {'model': "ClientError('An error occurred (404) when calling the HeadObject operation: Not Found')"}`

    ***ANS***: `export RUN_ID=YOUR_RUN_ID`
6. `Error response from daemon: driver failed programming external connectivity on endpoint integration-test-backend-1 (64fec1e2d167699754312ba77a8a7da4dde1031372c81088e6f2201ff9340acd): Bind for 0.0.0.0:8080 failed: port is already allocated`

    ***ANS***: PORT 8080:8080 is already allocated, so `docker ps` and `docker stop CURRENT_8080_PID
7. `zsh: permission denied: ./run.sh`

     ***ANS***: `chmod +x FILE_ADDRESS`

8. `ERROR: failed to solve: process "/bin/sh -c pipenv install --system --deploy" did not complete successfully: exit code: 1` when run bash `run.sh` file.

    ***ANS***: Since `pipenv` installs the dependency from `Pipfile.lock`, here is expected to update `Pipfile.lock` with `pipenv install Pipfile`. and then re-run `./run.sh`


9. When redeploy the kinesis stream in localstack `An error occurred (ResourceInUseException) when calling the CreateStream operation: Stream ride_preditions already exists`

    ***ANS***: Rename the current stream, or delete the existed stream at the endpoint.
    ```
    aws --endpoint-url=http://localhost:4566 \
   --region=ca-central-1 \
    kinesis delete-stream --stream-name ride_preditions

   ```

10. Check the kinesis stream from AWS/LOCALSTACK:`aws kinesis list-streams`/`aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams`

11. Pre-commit fails to install with error `An unexpected error has occurred: CalledProcessError: command: ('/Users/amberm/.cache/pre-commit/reposbydn2wf/py_env-python3/bin/python', '-mpip', 'install', '.')
return code: 1 .......`
    ***ANS***: Check the version of the hooks for installation. (I upgraded isort to 5.12.0 while the demo was 5.10.1)