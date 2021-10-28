from flask import Blueprint, render_template, request
from database import Database
from utils import parse_results
from services.table_service import TableService
from math import ceil

table_controller = Blueprint("table_controller", __name__)

database = Database()
table_service = TableService(database)


@table_controller.get("/")
def get_tables():
    tables = table_service.get_tables()
    return render_template("index.html", tables=tables)


@table_controller.get("/tables/<tablename>")
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


@table_controller.post("/tables/<tablename>")
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
