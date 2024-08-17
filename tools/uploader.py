import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from botocore.config import Config
import os


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._last_reported_percent = 0

    def __call__(self, bytes_amount):
        # To simplify, we'll assume this is hooked up to a single filename
        self._seen_so_far += bytes_amount
        percentage = int(self._seen_so_far / self._size * 100)
        if percentage != self._last_reported_percent:
            self._last_reported_percent = percentage
            print("Upload progress for %s: %s%%" % (self._filename, self._last_reported_percent))


class S3Uploader:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, bucket, debug=False):
        self.__session = boto3.session.Session()
        self.__bucket = bucket
        self.__aws_access_key = aws_access_key_id
        self.__debug = debug
        self.__s3 = self.__session.client(
            service_name='s3',
            config=Config(retries={'max_attempts': 10}),
            endpoint_url='https://storage.yandexcloud.net',
            region_name=str(region_name),
            aws_access_key_id=str(self.__aws_access_key),
            aws_secret_access_key=str(aws_secret_access_key),
        )

        self.__directory = datetime.now().strftime('%Y-%m-%d/%H_%M/')

        if self.__debug:
            print("Uploding to ", self.__directory)

    def apply(self, file_name):
        if not self.__debug:
            name = file_name.split('/')[-1]
            try:
                self.__s3.upload_file(file_name, self.__bucket, self.__directory + name, Callback=ProgressPercentage(file_name))
                print(file_name, "uploaded")
            except FileNotFoundError:
                print("The file was not found")
            except NoCredentialsError:
                print("Credentials not available")

        try:
            os.remove(file_name)
            print(file_name, "deleted!")
        except OSError as e:
            print("Error: %s : %s" % (file_name, e.strerror))