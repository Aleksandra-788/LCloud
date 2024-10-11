import boto3
import os
from dotenv import load_dotenv
import re
from botocore.exceptions import NoCredentialsError, ClientError
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = 'developer-task'
PREFIX = 'a-wing/'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_REGION)


def list_files():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    if 'Contents' in response:
        files = [file['Key'] for file in response['Contents']]
        print("Files in bucket:")
        for file in files:
            print(file)
    else:
        print("No files found.")


def upload_file(local_file, bucket_name):
    object_name = f'a-wing/{os.path.basename(local_file)}'
    try:
        s3 = boto3.client('s3')
        s3.upload_file(local_file, bucket_name, object_name)
        print(f"The file {local_file} has been successfully uploaded as {object_name}.")
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")


upload_file('test_file.txt', BUCKET_NAME)

