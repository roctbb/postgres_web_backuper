import os
import pyzipper
from config import ZIP_PASSWORD

class Archiver:
    def __init__(self, compression=5):
        self.compression = compression

    def apply(self, filename):
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)

        outfile = os.path.join(backup_dir, os.path.basename(filename) + '.zip')

        if not os.path.exists(filename):
            print(f"File or directory '{filename}' does not exist.")
            return None

        if os.path.isdir(filename):
            with pyzipper.AESZipFile(outfile, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
                zipf.setpassword(ZIP_PASSWORD.encode('utf-8'))
                for root, _, files in os.walk(filename):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, filename))
            return outfile
        else:
            with pyzipper.AESZipFile(outfile, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
                zipf.setpassword(ZIP_PASSWORD.encode('utf-8'))
                zipf.write(filename, os.path.basename(filename))

            os.remove(filename)
            return outfile