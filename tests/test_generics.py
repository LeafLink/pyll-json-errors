"""pyll_json_errors.generics"""
import pytest

from pyll_json_errors import generics


def test___generic_error_array():
    title = "title"
    detail = "detail"
    status = 200
    array = generics._generic_error(title, detail, status)
    assert array.errors[0].detail == detail
    assert array.errors[0].title == title
    assert array.errors[0].status == status


@pytest.mark.parametrize(
    "func, status, title",
    [
        (generics.error403, 403, "Forbidden"),
        (generics.error404, 404, "Not found"),
        (generics.error400, 400, "Bad Request"),
    ],
)
def test__generic_errors(func, status, title):
    err = func()
    assert err.errors[0].status == status
    assert err.errors[0].title == title
