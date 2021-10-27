def parse_schema(schema: list) -> list:
    parsed = []

    for (_, column, type, *__) in schema:
        parsed.append({"column": column, "type": type})

    return parsed


def parse_results(results: list, raw_schema: list):
    parsed_schema = parse_schema(raw_schema)
    parsed_results = []

    for result in results:
        parsed = {}

        for index, item in enumerate(parsed_schema):
            parsed[item["column"]] = result[index]

        parsed_results.append(parsed)

    return [parsed_results, parsed_schema]
