from typing import Dict


def get_all_occurences(field_name: str, dict_in: Dict):
    """Return a list of all values with the given field 
    name in an arbitrarily sized/nested dictionary
    """
    if hasattr(dict_in,'items'):
        for k, v in iter(dict_in.items()):
            if k == field_name:
                yield v
            if isinstance(v, dict):
                for result in get_all_occurences(field_name, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in get_all_occurences(field_name, d):
                        yield result