def parse_schema(schema: list) -> list:
    parsed = []

    for (_, column, column_type, *__) in schema:
        parsed.append({"column": column, "type": column_type})

    return parsed


def parse_results(results: list, schema: list):
    parsed_results = []

    for result in results:
        parsed = {}

        for index, item in enumerate(schema):
            parsed[item["column"]] = result[index]

        parsed_results.append(parsed)

    return parsed_results


def parse_query(results: list, column_names: list):
    parsed_query = []

    for result in results:
        parsed = {}

        for key, value in zip(column_names, result):
            parsed[key] = value

        parsed_query.append(parsed)

    return parsed_query


def parse_column_names(columns: list):
    return [name for (name, *_) in columns]
