import boto3

from datetime import datetime

import  os

class S3Uploader:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, bucket, debug=False):
        self.__session = boto3.session.Session()
        self.__bucket = bucket
        self.__aws_access_key = aws_access_key_id
        self.__debug = debug
        self.__s3 = self.__session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            region_name=str(region_name),
            aws_access_key_id=str(self.__aws_access_key),
            aws_secret_access_key=str(aws_secret_access_key),
        )

        self.__directory = datetime.now().strftime('%Y-%m-%d/%H_%M/')

    def apply(self, file_name):
        if not self.__debug:
            name = file_name.split('/')[-1]
            self.__s3.upload_file(file_name, self.__bucket, self.__directory + name)
            print(file_name, "uploaded")
        os.remove(file_name)
        print(file_name, "deleted!")