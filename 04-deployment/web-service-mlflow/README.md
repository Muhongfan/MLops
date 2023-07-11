Here, using locally hosted sqlite database for tracking server and s3 bucket for artifact storage. 
For that as a prerequisite create an S3 bucket and EC2 instance being used has access to the S3 bucket. 
***pre***: Install `aws` CLI:  
``` 
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```
1. To confirm try the following command and see you are able to get the list of buckets.

`aws s3 ls`
### Notes:
ERROR: ' Unable to locate credentials. You can configure credentials by running "aws configure". '
    1). Check configure list if the credential is already set, `aws configure list`
    2). (optional) If it does not, and shows as follow, set the `config` file.
    ![awsconfig.png](imgs%2Fawsconfig.png)
   
       `aws configure`
       ### Note: 
      - AWS Access Key ID [None]: The access key id from IAM 
      - AWS Secret Access Key [None]: The Secret key id from IAM
      - default region name should be the similar format as: `ca-central-1`

2. Run the following to start the mlflow tracking server

    `mlflow server  --backend-store-uri sqlite:///mlflow.db --default-artifact-root=s3://zoomcamp-mlops/`

    ***zoomcamp-mlops*** is the name of the S3 bucket I created in `[03-orchestration](..%2F..%2F03-orchestration)` which is for artifact storage.
### Note: if an error reported as"MlflowException: API request to endpoint /api/2.0/mlflow/experiments/get-by-name failed with error code 403 != 200. Response body: ''", it is because mlflow did not start.
3. Train the model in local environment. And check the experiment details and logged model artifact in mlflow UI ( http://127.0.0.1:5000/)
![awsartifact.png](imgs%2Fawsartifact.png)
![mlflowartifact.png](imgs%2Fmlflowartifact.png)
