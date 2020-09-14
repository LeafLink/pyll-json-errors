"""Helpful utility functions."""


def flatten_dict(*, data):
    """Flatten a nested dictionary into a tuple of tuples containing the key and value for each member of original dict.

    Useful for generating JSON pointers from dictionaries. Output contains flattened keys and flattens any iterable
    values.

    Args:
        data (dict): A dictionary to flatten.

    Returns:
        tuple: A tuple of tuples containing a tuple of str and a value.

    Example:
        .. code-block:: python

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
            outp = flatten_dict(data=inp)
            # outp
            # (
            #     (("simpleError",), "red"),
            #     (("simpleErrorList",), "orange"),
            #     (("simpleErrorList",), 1),
            #     (("objectError", "a"), "yellow"),
            #     (("objectError", "b"), 2),
            #     (("objectError", "c"), "green"),
            #     (("objectError", "c"), 3),
            #     (("1",), "blue"),
            #     (("2",), "purple"),
            #     (("2",), "4"),
            #     (("listedObjects", "0", "1"), "lime"),
            #     (("listedObjects", "0", "2"), "maroon"),
            #     (("listedObjects", "0", "2"), 5),
            #     (("listedObjects", "1", "3"), "pink"),
            #     (("listedObjects", "1", "d"), "jade"),
            #     (("listedObjects", "1", "d"), 6),
            # )
    """

    def _flatten(data2, flat_key):
        """Recursively go thru a dict and flatten."""
        if isinstance(data2, dict):
            """If data is a dict, recurse for each key in data."""
            for key in data2:
                yield from _flatten(data2[key], flat_key + [str(key)])
        elif isinstance(data2, (set, list, tuple)):
            """If data is an iterable, check type of each value in data"""
            for index, member in enumerate(data2):
                if isinstance(member, dict):
                    """If a dict, recurse with key. (Handles errors where there are list of nested objects."""
                    yield from _flatten(member, flat_key + [str(index)])
                else:
                    """else flatten without index b/c errors in member are for the same field."""
                    yield from _flatten(member, flat_key)
        else:
            yield flat_key, data2

    return tuple(tuple([tuple(key), value]) for key, value in _flatten(data, []))
