from sql_viewer.errors import Result


def monadic(function):
    def decorated(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return Result(result, None)
        except Exception as error:
            return Result(None, error)

    return decorated
