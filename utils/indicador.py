import re


def id_indicador(text):
    pattern = r"\.(\d+)\."

    match = re.search(pattern, text)

    if match:
        return int(match.group(1))
    else:
        return None
