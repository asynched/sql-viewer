from flask import jsonify


class Response:
    def __new__(cls, data: dict, status: int):
        return jsonify(data), status
