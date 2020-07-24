"""
Internal Python library to implement LeafLink flavored JSON API errors in HTTP APIs.

.. include:: ./documentation.md
"""
import importlib.util


def _check_dependency(importee, importer):
    """Helper method to determine if a python package is installed.

    Used in contrib modules to prevent importing base on optional dependencies.

    Args:
        importee (str): The module to import.
        importer (str): The name of the module importing `importee`.

    Returns:
        None

    Raises:
        ModuleNotFoundError
    """
    if importlib.util.find_spec(importee) is None:
        raise ModuleNotFoundError(f"'{importee}' optional dependency must be installed to use {importer}.")


__version__ = "0.1.0"
