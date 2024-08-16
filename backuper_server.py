from flask import Flask, request, redirect, jsonify, send_file
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from methods import *
from config import TP_login, TP_password
import os
import psycopg2

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

db_string = "postgresql://{}:{}@{}:{}/{}".format(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, "backuper")
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db.init_app(app)

migrate = Migrate(app, db)
auth = HTTPBasicAuth()

users = {
    TP_login: generate_password_hash(TP_password)
}


@app.route('/', methods=['get'])
@auth.login_required
def index():
    return send_file("templates/test.html")


@app.route('/api/databases', methods=['get'])
@auth.login_required
def get_databases():
    targets = get_schemas()
    records = create_records(targets)
    groups = get_groups(records)

    return jsonify(groups)

@app.route('/api/directories', methods=['GET'])
@auth.login_required
def get_directories_api():

    directories = get_directories()
    print(directories)
    return jsonify(directories)


@app.route('/api/save', methods=['POST'])
@auth.login_required
def save():
    Schema.query.update({Schema.mode: 'never'})
    db.session.commit()

    data = request.get_json()

    for database in data:
        if database["enabled"]:
            print(database)
            for schema in database["schemas"]:
                if schema["enabled"]:

                    record = Schema.query.filter_by(database=database["name"], schema=schema["name"]).first()
                    if not record:
                        record = Schema(database=database["name"], schema=schema["name"])
                        db.session.add(record)

                    record.mode = schema["mode"]
                    record.delete_days = schema["delete_days"]

    db.session.commit()
    return redirect("/")

@app.route('/api/save_direct', methods=['POST'])
@auth.login_required
def save_directories():

    Directory.query.delete()
    db.session.commit()

    data = request.get_json()

    for directory in data:

        print(directory)

        record = Directory.query.filter_by(path=directory["path"]).first()
        if not record:
            record = Directory(path=directory["path"])
            db.session.add(record)

        record.mode = directory["mode"]
        record.delete_days = directory["delete_days"]

    db.session.commit()
    return redirect("/")


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return "Sucsses"


if __name__ == '__main__':
    app.run(port=8080, debug=True, host="0.0.0.0")
