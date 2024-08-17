import os
from config import *
from tools import S3Uploader

objects = [os.path.join("backups", file) for file in os.listdir("backups") if
              os.path.isfile(os.path.join("backups", file))]

tools = [S3Uploader(S3_REGION, S3_access_key_id, S3_secret_access_key, S3_bucket, DEBUG)]

for tool in tools:
    print(objects, tool.__class__)
    objects = [object for object in list(map(tool.apply, objects)) if object]
