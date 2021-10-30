from flask import Blueprint, render_template, request
from sql_viewer.database import Database
from sql_viewer.services.table_service import TableService

table = Blueprint("table_controller", __name__, url_prefix="/")
table_service = TableService(Database())


@table.get("/")
def get_tables():
    tables = table_service.get_tables().flat()
    return render_template("index.html", tables=tables)


@table.get("/tables/<tablename>")
def get_table(tablename):
    database_schema = table_service.get_database_schema().flat()
    entries = table_service.get_table_entries(tablename).flat()

    return render_template(
        "table.html",
        tablename=tablename,
        entries=entries,
        database_schema=database_schema,
        items=entries.items,
        time=entries.time,
    )


@table.get("/editor")
def get_editor():
    database_schema = table_service.get_database_schema().flat()

    return render_template("editor.html", database_schema=database_schema)


@table.post("/editor")
def execute_editor_query():
    query = request.form.get("query")
    database_schema = table_service.get_database_schema().flat()
    entries = table_service.execute_query(query).flat()

    return render_template(
        "editor.html",
        database_schema=database_schema,
        entries=entries,
        items=entries.items,
        time=entries.time,
    )
