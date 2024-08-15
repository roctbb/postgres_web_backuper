import subprocess
from config import *


class Backuper:
    def __init__(self, user, password, host, port):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    def apply(self, target):
        db, schema = target
        filename = f"{db}_{schema}.sql"
        local_file_path = 'backups/{}'.format(filename)

        cmd = [
            PG_DUMP,
            '--dbname=postgresql://{}:{}@{}:{}/{}'.format(self.__user, self.__password, self.__host, self.__port, db),
            '-n', schema,
            '-f', local_file_path,
            '-v'
        ]

        if DEBUG:
            print(" ".join(cmd))

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error in backup creation: {stderr.decode('utf-8')}")
            return None

        return local_file_path
