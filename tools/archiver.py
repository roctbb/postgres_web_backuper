import os
import zipfile
from config import ZIP_PASSWORD

class Archiver:
    def __init__(self, compression=5):
        self.__compression = compression

    def apply(self, filename):
        outfile = filename + '.zip'

        with zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.setpassword(ZIP_PASSWORD.encode('utf-8'))
            zipf.write(filename, os.path.basename(filename))

        os.remove(filename)
        return outfile
