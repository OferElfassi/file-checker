from datetime import datetime
import json
import requests
import os
import re
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
slack_general = 'XXXXXXXXXXXXXXXXXXXXXXX'
slack_logs = 'XXXXXXXXXXXXXXXXXXXXXXX'


def has_numbers(inputString):
    res = inputString.split('/')[-1]
    return bool(re.search(r'\d', res))


def message_to_slack(msg, dest_url):
    slack_message = {'text': msg}
    response = requests.post(
        dest_url, data=json.dumps(slack_message),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        logger('Slack', 'Failed - {0}'.format(response.text))
    else:
        logger('Slack', 'Success - Message sent')


def logger(src, msg):
    log_msg = 'LOG DATE:{0} \nLOG SOURCE:{1} \n LOG CONTENT:{2} \n'.format(datetime.now(), src, msg)
    print(log_msg)
    message_to_slack(log_msg, slack_logs)


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False


def check_files():
    directory = '/home/ubuntu/projects/uploads'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # checking if it contains digits
            if has_numbers(f):
                uploaded = upload_to_aws(f, 'invalid-bucket', '{0}-{1}'.format(filename, datetime.now()))
                logger('File Checker', 'Failed - The file {0} was invalid'.format(filename))
                message_to_slack('The file {0} is corrupted, uploaded to the invalid bucket', slack_general)
            else:
                uploaded = upload_to_aws(f, 'valid-bucket', '{0}-{1}'.format(filename, datetime.now()))
                logger('File Checker', 'Failed - The file {0} was valid'.format(filename))
            if uploaded:
                os.remove(f)
                logger('AWS-S3', 'Upload Success')
            else:
                logger('AWS-S3', 'Failed to upload the file {0} to S3'.format(filename))


if __name__ == '__main__':
    print("CRON executed at - {0}\n".format(datetime.now().strftime("%D %H:%M:%S")))
    check_files()
