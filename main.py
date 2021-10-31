import logging
from flask import Flask
from rich.logging import RichHandler
from sql_viewer.controllers.table_controller import table as table_controller
from sql_viewer.controllers.api_controller import api as api_controller

logging.basicConfig(
    level="NOTSET",
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[
        RichHandler()
    ]
)

app = Flask(
    __name__,
    template_folder="sql_viewer/templates",
    static_folder="sql_viewer/static",
)

app.register_blueprint(table_controller)
app.register_blueprint(api_controller)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
