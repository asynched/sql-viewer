from flask import Blueprint
from sql_viewer.database import Database
from sql_viewer.utils.http import Response
from sql_viewer.services.api_service import APIService

api = Blueprint("api", __name__, url_prefix="/api")
api_service = APIService(Database())


@api.get("/database/schema")
def get_database_schema():
    result = api_service.get_database_schema()

    if result.error:
        return Response({"error": str(result.error)}, status=500)

    return Response(result.data, status=200)


@api.get("/database/schema/<tablename>")
def get_table_schema(tablename: str):
    result = api_service.get_table_schema(tablename)

    if result.error:
        return Response({"error": str(result.error)}, status=500)

    if result.data.items == 0:
        return Response(
            {"error": f"Table named '{tablename}' does not exist"},
            status=500,
        )

    return Response(
        {
            "table": tablename,
            "schema": result.data.json,
            "time": result.data.time,
            "items": result.data.items,
        },
        status=200,
    )


@api.get("/tables/<tablename>")
def get_table(tablename: str) -> Response:
    result = api_service.get_table(tablename)

    if result.error:
        return Response({"error": str(result.error)}, status=500)

    return Response(result.data.full_json, status=200)


@api.get("/tables")
def get_table_list():
    result = api_service.get_table_list()

    if result.error:
        return Response({"error": str(result.error)}, status=500)

    return Response(result.data.full_json, status=200)
