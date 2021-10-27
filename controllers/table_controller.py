from flask import Blueprint, render_template, request
from database import Database
from utils import parse_results, parse_schema
from math import ceil

table_controller = Blueprint("table_controller", __name__)

database = Database()


@table_controller.get("/")
def get_tables():
    query = """
        SELECT
            name
        FROM
            sqlite_master
        WHERE
            type = 'table' AND
            name NOT LIKE 'sqlite_%';
    """

    results = database.cursor.execute(query).fetchall()

    parsed_results = [result for (result,) in results]

    print(parsed_results)

    return render_template("index.html", tablenames=parsed_results)


@table_controller.get("/<tablename>")
def get_table(tablename):
    offset = int(request.args.get("offset", 0))
    pagesize = int(request.args.get("pagesize", 16))

    schema_query = (
        """
        PRAGMA table_info(%s) 
    """
        % tablename
    )

    results_query = (
        """
        SELECT
            *
        FROM
            %s
        LIMIT
            ?, ?;
    """
        % tablename
    )

    pages_query = (
        """
        SELECT
            COUNT(*)
        FROM
            %s;
    """
        % tablename
    )

    raw_schema = database.cursor.execute(schema_query).fetchall()
    raw_results = database.cursor.execute(results_query, (offset, pagesize)).fetchall()
    raw_pages = database.cursor.execute(pages_query).fetchall()

    pages = ceil(raw_pages[0][0] / int(pagesize))

    [results, schema] = parse_results(raw_results, raw_schema)

    previous_page = offset - 1 if offset > 0 else 0
    next_page = offset + 1 if offset < pages - 1 else offset

    return render_template(
        "table_page.html",
        tablename=tablename,
        results=results,
        schema=schema,
        pages=pages,
        previous_page=previous_page,
        next_page=next_page,
    )
