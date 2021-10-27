from flask import Flask
from controllers.table_controller import table_controller

app = Flask(__name__, template_folder="templates", static_folder="static")

app.register_blueprint(table_controller, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
