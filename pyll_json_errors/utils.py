"""Helpful utility functions provided by library."""


def flatten_dict(*, data):
    """Flatten a nested dictionary into a one-level dictionary.

    Useful for generating JSON pointers from dictionaries.

    Args:
        data (dict): A dictionary to flatten.

    Returns:
        Dict[Tuple[str], Any]: A one-level dictionary, where nested keys are represented as string tuples.

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

    outp = flatten_dict(data=inp)
    # outp
    # {
    #     ("hello",): "world",
    #     ("foo",): [
    #         "baz",
    #         "bar"
    #     ],
    #     ("0", "1"): 11,
    #     ("0", "2", "python"): "django",
    #     ("0", "2", "ruby"): "rails",
    #     ("0", "2", "java"): [
    #         "spring",
    #         "faces"
    #     ],
    #     ("0", "2", "javascript", "frameworks"): [
    #         "vue",
    #         "react"
    #     ]
    # }
    ```
    """

    def _flatten(data2, flat_key):
        if isinstance(data2, dict):
            for key in data2:
                yield from _flatten(data2[key], flat_key + [str(key)])
        else:
            yield flat_key, data2

    return {tuple(key): value for key, value in _flatten(data, [])}
