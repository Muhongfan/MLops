# Unit test
**Step 1**: Coppy the folder `04-deployment/streaming` to `06-best-practice/code` with `cp -r 04-deployment/streaming 06-best-practice/code`

**Step 2**: Install the env as that in Module 4 with `pipenv install`

**Step 3**: Install pytest with `pipenv install --dev pytest`

**Step 4**: Install python test environment in Pycharm. Go to `Setting -> Tool -> Testing -> Default test runner: pytest`, test `pytest` in terminal to see if it works, or `pytest --version`.

**Step 5**: Create a `model_test.py` file, type `assert 1 == 1` in the file, and then run `pytest` in the terminal. If it works, it should be as follows:

![pytest.png](img%2Fpytest.png)

## Testing if docker works

**Step 6**: Build the docker and check if the service works.

Build the docker with `docker build -t stream-model-duration:v2 .` 

and run with
```
docker run -it --rm \
        -p 8080:8080 \
        -e PREDICTIONS_STREAM_NAME="ride_predictions" \
        -e RUN_ID="7c8bb75fadea44aa9337ec3de35c430e" \
        -e TEST_RUN="True" \
        -e AWS_DEFAULT_REGION="ca-central-1" \
        stream-model-duration:v2
```

then open another terminal, run `python test_docker.py`([test_docker.py](..%2F04-deployment%2Fstreaming%2Ftest_docker.py)
), the result should be as below:
![docker.png](img%2Fdocker.png)

**NOTE**: Run each test by running `pytest` in the terminal

### MODEL test

**Step 7**: Unit test (`test_prepare_features()`). Test if the model can take the raw data and returns the expected features.

### LOGIC / DECODE test
**Step 8**: Unit test (`test_base64_decode()`). Test if it can read the base64 encoded data and decodes it as expected.

### Predict function test

**Step 9**: Unit test (`test_predict()`). It creates a ModelService object with a ModelMock object, test if it predicts ride duration, and checks if it is as expected.

### Lambda handler test

**Step 10**: Unit test (`test_lambda_handler()`). Test if it handles a Lambda function event and the results are as expected. 


# Integration test
Unit tests just test partial of the code, whole we still need to test the whole code with integration test by docker. (Turn `test_docker.py` into a test)
## Capture the diffs between actual_response and expected_response
**Step 1**: Install `deepdiff` in `dev` with `pipenv install --dev deepdiff` and print the diffs of the data changes.
![diff.png](img%2Fdiff.png)

## Load the model first from local env, remove the dependency in S3
**Step 2**: Add `get_model_location()` and modigy `load_model()` to load the model from local folder
**Step 3**: Download the models from S3 to local `model/` with `aws s3 cp --recursive s3://zoomcamp-mlops/1/7c8bb75fadea44aa9337ec3de35c430e/artifacts/model/ model`
**Step 4**: Add the model local location and the address, then run `python test_docker.py` to test the model which has been downloaded in local env.
```
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_preditions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="ca-central-1" \
    -v $(pwd)/model:/app/model \
    stream-model-duration:v2
```

#  Test Automation
**Step 1**: Create a new file named `run.sh` under `integration-test`, and change the access permissions of it.
Using the `env` utility of `Shebang` in Bash Scripts. [Bash Shebang](https://linuxize.com/post/bash-shebang/)
```shell
chmod +x integration_test/run.sh
./run.sh
```
**Step 2**: Create `docker-compose.yaml` based on the format of [Compose file reference](https://docs.docker.com/compose/compose-file/06-networks/).
**Step 3**: Open a terminal in a non-virtual env, run `./run.sh`.
![RUNBASH.png](img%2FRUNBASH.png)

### RUN.SH
```SHELL
#!/usr/bin/env bash
set -e

cd "$(firname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} ..

docker compose up -d

sleep 1

pipenv run python test_docker.py

ERROR_CODE=$?

if [${ERROR_CODE} != 0]; then
  docker compose logs
fi

docker compose down
exit ${ERROR_CODE}


```
- `set -e`: bash script interrupted on error
- `cd "$(firname "$0")"`: get path of the script 
- `LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
`: maintain the build version
- `docker build -t ${LOCAL_IMAGE_NAME} ..`: build the image
- `docker compose up -d`: start docker compose
- `ERROR_CODE=$?`: reads the exit status of the last command executed
- `if [${ERROR_CODE} != 0]; then
  docker compose logs
fi`: if there is an error, print the docker logs
- `docker compose down`: stops containers and removes containers

### DOCKER-COMPOSE.YAML
```SEHLL
services:
  backend:
    image: ${LOCAL_IMAGE_NAME}
    ports:
      - "8080:8080"
    environment:
      - PREDICTIONS_STREAM_NAME=ride_preditions
      - TEST_RUN=True
      - RUN_ID=Test123
      - AWS_DEFAULT_REGION=ca-central-1
      - MODEL_LOCATION=/app/model
    volumes:
      - "./model:/app/model"
```

# Could service test with LocalStack (Kinesis CallBacks)
Test the Kinesis connection or the function that puts the responses to the Kinesis stream with LocalStack
**Step 1**: Download localstack. 
Add ```  kinesis:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=kinesis``` into `docker-compose.yaml` and run `docker compose up kinesis`
**Step 2**: Create streams in localstack with 
```
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ride_preditions \
    --shard-count 1
    
```
**Step 3**: Check the content in the stream. Export `SHARD` and `PREDICTIONS_STREAM_NAME` ahead of time.
```
 aws  --endpoint-url=http://localhost:4566 \
    kinesis     get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --query 'ShardIterator'
```
and get the results back.

![kinesis_stream.png](img%2Fkinesis_stream.png)

then get the shard iterator and decode it.

```shell
 aws  --endpoint-url=http://localhost:4566 \
    kinesis get-records --shard-iterator "AAAAAAAAAAFWPQ+4NtNa8s85Qzsl/rDfUyuw9d9svafo+/IH7m4FgT6zIx0dxeAzqZV2s6SmJDcihSWsUHD48T+v2Y5rOHqeFQm/IAIcjMFOI+k4mGvyJbHcNGtTuy/9WP38ZjmmAH2xcDX9oMk/0Z/f8Jj2S4TmGRsBcXJMURHYD3NRNy95Jnb9opAa+OlSepTPaGfyp7OF3wBLVpx1OM0Nh7b4d0Dr"
```

check the streams in endpoint with `aws --endpoint-url=http://localhost:4566 \`   kinesis list-stream `

**Step 4**: Transform the above steps into auto-test.[test_kinesis.py](code%2Fintegration-test%2Ftest_kinesis.py)

**Step 5**: Edit the logic in `run.sh`: if `test_docker.py` does not work, then exit; or continue `test_kinesis.py` for the work.
```shell
pipenv run python test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi


pipenv run python test_kinesis.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down
```
**Step 6**: Run `python test_kinesis.py`.



# Code quality Test with pylint
**Step 1**: Install pylint for code quality check with `pipenv install --dev pylint`
**Step 2**: Check the code quality of a file with `pylint model.py`, or all the files under the current folder with `pylint **/*.py`.
**Step 3**: (Configuration of `black` and `isort` is also available in `pyproject.toml`)Code formatting with `Black`, sorting import with `isort` with `pipenv install --dev black isort`. Run `black .`/`isort .` for formatting/sorting the code/import and show differences after formatting/sorting with `black --diff . | less`/`isort --diff . | less`.

# Git pre-commit
**Step 1**: Install pre-commit 
```
git init
pipenv install --dev pre-commit

```
**Step 2**: Initial the `./code` as a new git repo for `pre-commit` check. Get the `sample-config` as `.pre-commit-config.yaml` with `pre-commit sample-config > ./pre-commit-config.yaml`
**Step 3**: Install pre-commit hooks `pre-commit install`

**Step 4**: Add the files to repo and commit for `pre-commit` check with 
```
git add . 
git commit -m `YOUR_COMMIT`
```
The result should be as:
![precommit.png](img%2Fprecommit.png)


# Makefile
**Note:** 
1. Mac already installed `make`
2. Makefile must start with a tab

Arrange the [Makefile](code%2FMakefile) with the requirement, and run it with `make run`. 
Run any of these targets by typing `make <target>` as `make quality_checks`.



### Note:
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