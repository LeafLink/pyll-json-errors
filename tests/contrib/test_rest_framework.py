"""pyll_json_errors.contrib.rest_framework"""
import pytest
from werkzeug.http import HTTP_STATUS_CODES

from django.conf import settings
from django.test import RequestFactory

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from pyll_json_errors.contrib import rest_framework
from pyll_json_errors import constants


def test__make_response(json_error_array_factory):
    """
    Ensure `rest_framework.make_response` returns a DRF Response object with the
    correct status.
    """
    error_array = json_error_array_factory()
    response = rest_framework.make_response(error_array)
    assert isinstance(response, Response)
    assert response.status_code == error_array.status


@pytest.mark.parametrize(
    "exc,formatted",
    [
        [
            ValidationError({"field1": ["bad", "very bad"]}),
            [
                {
                    "title": HTTP_STATUS_CODES.get(400),
                    "code": "invalid",
                    "detail": "bad",
                    "source": {"pointer": "/field1"},
                    "status": "400",
                },
                {
                    "title": HTTP_STATUS_CODES.get(400),
                    "code": "invalid",
                    "detail": "very bad",
                    "source": {"pointer": "/field1"},
                    "status": "400",
                },
            ],
        ],
        [
            ValidationError({"field2": "also bad"}),
            [
                {
                    "title": HTTP_STATUS_CODES.get(400),
                    "code": "invalid",
                    "detail": "also bad",
                    "source": {"pointer": "/field2"},
                    "status": "400",
                }
            ],
        ],
        [
            ValidationError({"list": [{"bad": "1"}, {"bad": "2"}]}),
            [
                {
                    "title": HTTP_STATUS_CODES.get(400),
                    "code": "invalid",
                    "detail": "1",
                    "source": {"pointer": "/list/0/bad"},
                    "status": "400",
                },
                {
                    "title": HTTP_STATUS_CODES.get(400),
                    "code": "invalid",
                    "detail": "2",
                    "source": {"pointer": "/list/1/bad"},
                    "status": "400",
                },
            ],
        ],
    ],
)
def test__drf_transform(exc, formatted):
    """
    Ensure the transform works correctly with different layouts of nested errors, as seen
    above. It tests lists of details, flat errors, and nested lists.
    """
    transform = rest_framework.DRFTransform()
    error_array = transform.to_array(sources=[exc,])
    assert {"errors": formatted} == error_array.as_dict()


def test__reformat_response():
    """
    Ensure the custom error handler is functioning by calling it with a faked exception
    and context dictionary, including a faked request.
    """
    exc = ValidationError({"bad": "is bad"})
    request = RequestFactory().get("/thingo/")
    resp = rest_framework.reformat_response(exc, {"request": request})
    assert resp.status_code == 400
    assert resp.data == {
        "errors": [
            {
                "title": HTTP_STATUS_CODES.get(400),
                "status": "400",
                "code": "invalid",
                "detail": "is bad",
                "source": {"pointer": "/bad"},
            }
        ]
    }


def test__reformat_response_not_api_exception():
    """
    Ensure the custom error handler returns None when it cannot handle the api exception
    type.
    """
    exc = RuntimeError()
    request = RequestFactory().get("/thingo/")
    resp = rest_framework.reformat_response(exc, {"request": request})
    assert resp is None
