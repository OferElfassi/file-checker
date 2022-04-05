from datetime import datetime
import os
import re
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def has_numbers(inputString):
    res = inputString.split('/')[-1]
    return bool(re.search(r'\d', res))


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def check_files():
    directory = '/home/ubuntu/projects/uploads'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # checking if it contains digits
            if has_numbers(f):
                uploaded = upload_to_aws(f, 'invalid-bucket', '{0}-{1}'.format(f, datetime.now()))
                print('The file {0} was invalid\n{1}'.format(filename, uploaded))
            else:
                uploaded = upload_to_aws(f, 'valid-bucket', '{0}-{1}'.format(f, datetime.now()))
                print('The file {0} was valid\n{1}'.format(filename, uploaded))


if __name__ == '__main__':
    print("CRON executed at - \n")
    print(datetime.now().strftime("%D %H:%M:%S"))
    check_files()
