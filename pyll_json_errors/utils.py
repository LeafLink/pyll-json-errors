"""Helpful utility functions provided by library."""
from pyll_json_errors import constants


def flatten_dict(*, data, prefix=constants.JSON_POINTER_SEPARATOR, separator=constants.JSON_POINTER_SEPARATOR):
    """Flatten a nested dictionary into a one-level dictionary.

    Useful for generating JSON pointers from dictionaries.

    Args:
        data (dict): A dictionary to flatten.
        prefix (str): Some string to append at the beginning of each final flattened key.
        separator (str): String to use as the separator between each key part in final flattened keys.

    Returns:
        dict: A one-level dictionary.

    Examples:
    ```python
    inp = {
        "hello": "world",
        "foo": ["baz", "bar"],
        0: {
            1: 11,
            2: {
                "python": "django",
                "ruby": "rails",
                "java": ["spring", "faces"],
                "javascript": {
                    "frameworks": ["vue", "react"]
                }
            }
        }
    }

    outp = flatten_dict(data=inp, prefix="/" separator=".")
    # outp
    # {
    #     "/hello": "world",
    #     "/foo": [
    #         "baz",
    #         "bar"
    #     ],
    #     "/0.1": 11,
    #     "/0.2.python": "django",
    #     "/0.2.ruby": "rails",
    #     "/0.2.java": [
    #         "spring",
    #         "faces"
    #     ],
    #     "/0.2.javascript.frameworks": [
    #         "vue",
    #         "react"
    #     ]
    # }
    ```
    """

    def _flatten(data2, prefix2, separator2, flat_key):
        if isinstance(data2, dict):
            flat_key = f"{flat_key}{separator2}" if flat_key else flat_key
            for key in data2:
                yield from _flatten(data2[key], prefix2, separator2, f"{flat_key}{str(key)}")
        else:
            yield f"{prefix2}{flat_key}", data2

    return {key: value for key, value in _flatten(data, prefix, separator, "")}
