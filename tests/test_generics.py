"""pyll_json_errors.generics"""
import pytest

from pyll_json_errors import generics


def test___generic_error():
    title = "title"
    detail = "detail"
    status = 200
    err = generics._generic_error(title, detail, status)
    assert err.detail == detail
    assert err.title == title
    assert err.status == status


def test___generic_error_array():
    title = "title"
    detail = "detail"
    status = 200
    array = generics._generic_error_array([generics._generic_error(title, detail, status)])
    assert array.errors[0].detail == detail
    assert array.errors[0].title == title
    assert array.errors[0].status == status


@pytest.mark.parametrize(
    "func, status, title", [(generics.error403, 403, "Forbidden"), (generics.error404, 404, "Not found")]
)
def test__error403(func, status, title):
    err = func()
    assert err.errors[0].status == status
    assert err.errors[0].title == title
