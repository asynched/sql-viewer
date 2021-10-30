from itertools import chain


def flat(source: list) -> list:
    return list(chain(*source))
