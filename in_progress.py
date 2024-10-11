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


list_files()



