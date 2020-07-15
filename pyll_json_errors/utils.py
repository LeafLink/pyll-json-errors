from pyll_json_errors import constants


def flatten_dict(*, data, separator=constants.JSON_POINTER_SEPARATOR, prefix=""):
    """Flatten a nested dictionary into a one-level dictionary.

    Args:
        data (dict): A dictionary to flatten.
        separator (str): String to use as the separator between each key part in final keys.
        prefix (str): Some string to append at the beginning of final keys.

    Return:
        dict: A one-level dictionary.
    """
    return (
        {
            f"{prefix}{separator}{key}" if prefix else key: value
            for key2, value2 in data.items()
            for key, value in flatten_dict(data=value2, separator=separator, prefix=str(key2)).items()
        }
        if isinstance(data, dict)
        else {prefix: data}
    )
