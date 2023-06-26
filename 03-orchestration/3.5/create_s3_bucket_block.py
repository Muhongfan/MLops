from time import sleep
from prefect_aws import S3Bucket, AwsCredentials

def create_aws_creds_block():
    my_aws_creds_obj = AwsCredentials(
        # Your info
        aws_access_key_id = "_", aws_secret_access_key = "_/_"
    )
    my_aws_creds_obj.save(name="my-aws-creds", overwrite = True)
def crete_s3_bucket_block():
    aws_creds = AwsCredentials.load("my-aws-creds")
    my_s3_bucket_obj = S3Bucket(
        bucket_name = "my-first-bucket-abc", credentials = aws_creds
    )
    my_s3_bucket_obj.save(name = "s3-bucket-example", overwrite = True)

if __name__ == '__main__':
    create_aws_creds_block()
    sleep(5)
    crete_s3_bucket_block()
