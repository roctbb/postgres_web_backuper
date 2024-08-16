import psycopg2
from config import *
from models import *


def get_schemas():
    result = []
    try:
        conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database")
        databases = cursor.fetchall()
        cursor.close()
        conn.close()

    except Exception as error:
        print("Ошибка при работе с базой данных:", error)
        return []

    for database in databases:
        if database in IGNORED_DATABASES:
            continue
        try:
            conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
                                    database=database[0])

            cursor = conn.cursor()
            cursor.execute("SELECT schema_name FROM information_schema.schemata")

            schemas = cursor.fetchall()

            for schema in schemas:
                result.append((database[0], schema[0]))

            cursor.close()
            conn.close()
        except Exception as error:
            print("Ошибка при работе с базой данных:", error)

    return result


#############

def create_records(targets):
    for database, schema in targets:
        record = Schema.query.filter_by(database=database, schema=schema).first()
        if not record:
            db.session.add(Schema(database=database, schema=schema, mode="never"))
    db.session.commit()

    return Schema.query.all()


##############

def get_groups(records):
    databases = []

    for record in records:
        if record.database != "template1":
            database_entry = next((db for db in databases if db["name"] == record.database), None)
            if not database_entry:
                database_entry = {
                    "name": record.database,
                    "enabled": False,
                    "schemas": []
                }
                databases.append(database_entry)

            if record.schema not in IGNORED_SCHEMAS:

                schema_entry = next((schema for schema in database_entry["schemas"] if schema["name"] == record.schema),
                                    None)
                if not schema_entry:
                    if not record.mode:
                        record.mode = "never"

                    schema_entry = {
                        "name": record.schema,
                        "enabled": record.mode != "never",
                        "mode": record.mode ,
                        "delete_days": record.delete_days
                    }
                    database_entry["schemas"].append(schema_entry)

                    if record.mode != "never":
                        database_entry["enabled"] = True

    return sorted(databases, key=lambda d: d["name"])


###########################################################################################


def get_directories():
    result = []

    for directory in Directory.query:
        result.append({
            "id": directory.id,
            "path": directory.path,
            "mode": directory.mode,
            "delete_days": directory.delete_days
        })

    return result


##############

def create_directory_records(paths):
    for path in paths:
        record = Directory.query.filter_by(path=path).first()
        if not record:
            db.session.add(Directory(path=path, mode="default_mode", delete_days=None))
    db.session.commit()

    return Directory.query.all()


##############

def get_directory_groups(records):
    directory_groups = []

    for record in records:
        directory_entry = {
            "path": record.path,

            "mode": record.mode,
            "delete_days": record.delete_days,
        }
        directory_groups.append(directory_entry)

    return directory_groups
