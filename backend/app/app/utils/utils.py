from typing import Any, Dict


def get_all_occurences(field_name: str, dict_in: Dict):
    """Return a list of all values with the given field
    name in an arbitrarily sized/nested dictionary
    """
    if hasattr(dict_in, "items"):
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


def populate_each_instance(field_name: str, dict_in: Dict, **kwargs: Any):
    """Searches a nested dictionary for objects that contain the specified
    field name and then populates them each with each passed in keyword
    argument. If the object already has an instance of the keyword argument
    it is not overwritten.

    Example:
        Given the following object
        >> obj_in = {
            "task": "test",
            "kwargs": {
                "tasks": [
                    {
                        "task": "test",
                        "args": [1,2],
                        "options": {"eta": 3},
                    },
                    {
                        "task": "test",
                        "args": [1,2]
                    },
                ]
            }
        }

        Invoking this function with the object above
        >> obj_out = populate_each_instance("task", obj_in, options=dict())

        Will return the object as follows
        >> obj_out = {
            "task": "test",
            "kwargs": {
                "tasks": [
                    {
                        "task": "test",
                        "args": [1,2],
                        "options": {"eta": 3},
                    },
                    {
                        "task": "test",
                        "args": [1,2],
                        "options": {},
                    },
                ]
            },
            "options": {},
        }

    """
    if hasattr(dict_in, "items"):
        if field_name in dict_in:
            keys_to_add = kwargs.keys() - dict_in.keys()
            dict_in.update({key: kwargs[key] for key in keys_to_add})

        for v in dict_in.values():
            if isinstance(v, dict):
                populate_each_instance(field_name, v, **kwargs)
            elif isinstance(v, list):
                for d in v:
                    populate_each_instance(field_name, d, **kwargs)
