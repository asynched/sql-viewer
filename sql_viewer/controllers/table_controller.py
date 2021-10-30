from flask import Blueprint, render_template, request
from sql_viewer.database import Database
from sql_viewer.services.table_service import TableService

table = Blueprint("table_controller", __name__, url_prefix="/")
table_service = TableService(Database())


@table.get("/")
def get_tables():
    tables = table_service.get_tables()
    return render_template("index.html", tables=tables)


@table.get("/tables/<tablename>")
def get_table(tablename):
    database_schema = table_service.get_database_schema()
    schema = table_service.get_table_schema(tablename)
    entries = table_service.get_table_entries(
        tablename,
        schema=schema,
    )

    return render_template(
        "table.html",
        tablename=tablename,
        entries=entries,
        schema=schema,
        database_schema=database_schema,
    )


@table.post("/tables/<tablename>")
def execute_query(tablename: str):
    query = request.form.get("query")

    database_schema = table_service.get_database_schema()
    [entries, schema] = table_service.execute_query(query)

    return render_template(
        "table.html",
        tablename=tablename,
        entries=entries,
        schema=schema,
        database_schema=database_schema,
    )
