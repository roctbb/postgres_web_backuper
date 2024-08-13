from flask import Flask, render_template, request, redirect, jsonify, send_file
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from methods import *
from config import TP_login, TP_password
import os

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

@app.route('/databases', methods=['get'])
@auth.login_required
def get_databases():
    targets = get_schemas()
    records = create_records(targets)
    groups = get_groups(records)

    return jsonify(groups)

@app.route('/', methods=['post'])
@auth.login_required
def save():
    for database, schema in get_schemas():
        freq = request.form.get(f"frequency_{database}_{schema}")

        schema = Schema.query.filter_by(database=database, schema=schema).first()
        if schema and freq in ["daily", "weekly", "never"]:
            schema.freq = freq
    db.session.commit()

    return redirect("/")

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return "Sucsses"



if __name__ == '__main__':
    app.run(port=8080, debug=True, host="0.0.0.0")
