from models import *
from config import *
from tools import *


def make_backup(modes, files=True, databases=True):

    if databases:
        print("backuping dbs:")

        targets = Schema.query.all()

        objects = [(target.database, target.schema) for target in targets if target.mode in modes]
        tools = [Backuper(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT), Archiver(ZIP_PASSWORD), S3Uploader(S3_REGION, S3_access_key_id, S3_secret_access_key, S3_bucket, DEBUG)]

        for tool in tools:
            print(objects, tool.__class__)
            objects = list(map(tool.apply, objects))

    if files:
        print("backuping files:")

        targets_direct = Directory.query.all()

        objects = [target_direct.path for target_direct in targets_direct if target_direct.mode in modes]
        tools = [Archiver(ZIP_PASSWORD), S3Uploader(S3_REGION, S3_access_key_id, S3_secret_access_key, S3_bucket, DEBUG)]

        for tool in tools:
            print(objects, tool.__class__)
            objects = [object for object in list(map(tool.apply, objects)) if object]



