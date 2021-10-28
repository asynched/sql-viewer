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
