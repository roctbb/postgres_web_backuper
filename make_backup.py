# -*- coding: utf-8 -*-
from backuper_server import app
from methods import *

with app.app_context():
    backup_files = make_backup(modes=['daily', 'weekly'])
