"""Helpful utility functions provided by library."""


def flatten_dict(*, data):
    """Flatten a nested dictionary into a one-level dictionary.

    Useful for generating JSON pointers from dictionaries. Output contains flattened keys and flattens any iterateable
    values.

    Args:
        data (dict): A dictionary to flatten.

    Returns:
        Dict[Tuple[str], Any]: A one-level dictionary, where nested keys are represented as string tuples.

    Examples:
    ```python
    inp = {
        "simpleError": "red",
        "simpleErrorList": ["orange", 1],
        "objectError": {
            "a": "yellow",
            "b": 2,
            "c": ["green", 3]
        },
        1: "blue",
        2: ["purple", 4],
        "listedObjects": [
            {
                "1": "lime",
                2: ["maroon", 5]
            },
            {
                3: "pink",
                "d": ["jade", 6]
            }
        ]
    }
    # outp
    # outp = (
    #     ("/simpleError", "red"),
    #     ("/simpleErrorList/0", "orange"),
    #     ("/simpleErrorList/1", "1"),
    #     ("/objectError/a", "yellow"),
    #     ("/objectError/b", "2"),
    #     ("/objectError/c/0", "green"),
    #     ("/objectError/c/1", "3"),
    #     ("/1", "blue"),
    #     ("/2/0", "purple"),
    #     ("/2/1", "4"),
    #     ("/listedObjects/0/1", "lime"),
    #     ("/listedObjects/0/2/0", "maroon"),
    #     ("/listedObjects/0/2/1", "5"),
    #     ("/listedObjects/1/3", "pink"),
    #     ("/listedObjects/1/d/0", "jade"),
    #     ("/listedObjects/1/d/1", "6"),
    # )
    ```
    """

    def _flatten(data2, flat_key):
        if isinstance(data2, dict):
            for key in data2:
                yield from _flatten(data2[key], flat_key + [str(key)])
        elif isinstance(data2, (set, list, tuple)):
            for index, member in enumerate(data2):
                yield from _flatten(member, flat_key + [str(index)])
        else:
            yield flat_key, data2

    return {tuple(key): value for key, value in _flatten(data, [])}
