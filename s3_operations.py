import boto3
import os
from dotenv import load_dotenv
import re
from botocore.exceptions import NoCredentialsError, ClientError
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_REGION)


def list_files(bucket_name: str) -> None:
    """List all files in the bucket.
    Args:
        bucket_name (str): The name of the S3 bucket to list the files from.

    Returns:
        None. Prints the list of files in the specified bucket, or an appropriate message if no files are found.
    """
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            files = [file['Key'] for file in response['Contents']]
            print("Files in bucket:")
            for file in files:
                print(file)
        else:
            print("No files found.")
    except ClientError as e:
        print(f"Error listing files: {e}")


def upload_file(local_file: str, bucket_name: str) -> None:
    """Upload a local file to the S3 bucket at the given location.
    Args:
        local_file (str): The local file path to be uploaded.
        bucket_name (str): The name of the S3 bucket where the file will be uploaded.

    Returns:
        None. Prints a success message if the file was uploaded successfully, or an error message if something went
        wrong.
        """
    object_name = os.path.basename(local_file)
    try:
        s3.upload_file(local_file, bucket_name, object_name)
        print(f"The file {local_file} has been successfully uploaded as {object_name}.")
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")


def list_files_matching_regex(bucket_names: str, pattern: str) -> None:
    """List files in the S3 buckets that match the given pattern.
    Args:
        bucket_names (str): Bucket names in string format separated with commas to search through.
        pattern (str): The regex pattern to match file names.

    Returns:
        None. Prints the list of files that match the regex pattern, or an appropriate message if no matching files are
        found.
    """
    list_of_buckets = bucket_names.split(",")
    for bucket_name in list_of_buckets:
        try:
            response = s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                files = [file['Key'] for file in response['Contents']]
                matching_files = [f for f in files if re.match(pattern, f)]
                print("Files matching the regex pattern:")
                for file in matching_files:
                    print(file)
            else:
                print("No files found.")
        except ClientError as e:
            print(f"Error listing files: {e}")


def delete_files_matching_regex(bucket_name: str, pattern: str) -> None:
    """Delete all files in the S3 bucket that match the given pattern.
    Args:
        bucket_name (str): The name of the S3 bucket to delete files from.
        pattern (str): The regex pattern to match file names for deletion.

    Returns:
        None. Prints the number of files deleted, or an appropriate message if no matching files were found.
    """
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            files = [file['Key'] for file in response['Contents']]
            matching_files = [f for f in files if re.match(pattern, f)]
            if matching_files:
                delete_objects = {'Objects': [{'Key': f} for f in matching_files]}
                s3.delete_objects(Bucket=bucket_name, Delete=delete_objects)
                print(f"Deleted {len(matching_files)} files matching the regex.")
            else:
                print("No files matching the regex found.")
        else:
            print("No files found.")
    except ClientError as e:
        print(f"Error deleting files: {e}")
