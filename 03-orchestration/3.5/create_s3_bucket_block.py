from time import sleep
from prefect_aws import S3Bucket, AwsCredentials


def create_aws_creds_block():
    my_aws_creds_obj = AwsCredentials(

        # Your info
        aws_access_key_id = "_", aws_secret_access_key = "_/_"
    )
    my_aws_creds_obj.save(name="mlops-zoom-user", overwrite=True)

def create_s3_bucket_block():
    aws_creds = AwsCredentials.load("mlops-zoom-user")
    my_s3_bucket_obj = S3Bucket(
        bucket_name="zoomcamp-mlops", credentials=aws_creds
    )
    my_s3_bucket_obj.save(name="zoomcamp-mlops", overwrite=True)


if __name__ == "__main__":
    create_aws_creds_block()
    sleep(5)
    create_s3_bucket_block()
