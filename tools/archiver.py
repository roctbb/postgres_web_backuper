import os
import pyzipper  # Убедитесь, что pyzipper установлен

class Archiver:
    def __init__(self, password):
        self.__password = password

    def apply(self, filename):
        outfile = filename + '.zip'

        # Создание ZIP-файла с шифрованием
        with pyzipper.AESZipFile(outfile, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
            zipf.pwd = self.__password.encode('utf-8')
            zipf.write(filename, os.path.basename(filename))  # Добавление файла в архив


        os.remove(filename)  # Удаление исходного файла

        return outfile
