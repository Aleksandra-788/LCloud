import sys
from s3_operations import list_files, upload_file, list_files_matching_regex, delete_files_matching_regex


def main():
    if len(sys.argv) < 3:
        print("Usage: python cli.py [list|upload|list_regex|delete_regex] <bucket_name> [additional_args] ")
        sys.exit(1)

    command = sys.argv[1]
    bucket_name = sys.argv[2]

    if command == 'list':
        list_files(bucket_name)

    elif command == 'upload':
        local_file = sys.argv[3]
        upload_file(local_file, bucket_name)

    elif command == 'list_regex':
        bucket_names = sys.argv[3]
        pattern = sys.argv[4]
        list_files_matching_regex(bucket_names, pattern)

    elif command == 'delete_regex':
        pattern = sys.argv[3]
        delete_files_matching_regex(bucket_name, pattern)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
