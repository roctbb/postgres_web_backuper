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


def create_records(targets):
    for database, schema in targets:
        record = Schema.query.filter_by(database=database, schema=schema).first()
        if not record:
            db.session.add(Schema(database=database, schema=schema, freq="never"))
    db.session.commit()

    return Schema.query.all()


def get_groups(records):
    databases = []

    for record in records:
        if record.database != "template1":
            database_entry = next((db for db in databases if db["name"] == record.database), None)
            if not database_entry:

                database_entry = {
                    "name": record.database,
                    "enabled": True,
                    "schemas": []
                }
                databases.append(database_entry)

            # Проверяем, не находится ли схема в списке игнорируемых
            if record.schema not in IGNORED_SCHEMAS:
                # Поиск существующей схемы в текущей базе данных
                schema_entry = next((schema for schema in database_entry["schemas"] if schema["name"] == record.schema), None)
                if not schema_entry:
                    # Если схема не найдена, создаем новый объект схемы
                    schema_entry = {
                        "name": record.schema,
                        "enabled": True,
                        "mode": record.mode,
                        "delete_days": record.delete_days
                    }
                    database_entry["schemas"].append(schema_entry)

    return databases

