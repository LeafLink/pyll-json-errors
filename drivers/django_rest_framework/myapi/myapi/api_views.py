from django.http.response import Http404
from rest_framework import decorators, exceptions


@decorators.api_view(["GET"])
def error_403(request):
    """Returns a 403 json api formatted error.

    {
        errors: [
            {
                status: "403",
                code: "permission_denied",
                title: "Forbidden",
                detail: "You do not have permission to perform this action."
            }
        ]
    }
    """
    raise exceptions.PermissionDenied()


@decorators.api_view(["GET"])
def error_404(request):
    """Return a DRF 404 json api formatted error.

    {
        errors: [
            {
                status: "404",
                code: "not_found",
                title: "Not Found",
                detail: "Not found."
            }
        ]
    }
    """
    raise exceptions.NotFound()


@decorators.api_view(["GET"])
def error_404_django(request):
    """Return a django 404 json api formatted error.

    {
        errors: [
            {
                status: "404",
                code: "not_found",
                title: "Not Found",
                detail: ""
            }
        ]
    }
    """
    raise Http404()


@decorators.api_view(["GET"])
def error_500(request):
    """Return a django 500 error, not json api formatted."""
    raise RuntimeError("an error")


@decorators.api_view(["GET"])
def error_400(request):
    """Return a nested 400 json api formatted error.

    {
        errors: [
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "this field is bad 1",
                source: {
                    pointer: "/bad"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "this field is bad 2",
                source: {
                    pointer: "/bad"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "this field is also bad",
                source: {
                    pointer: "/price/amount"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "bad, but less bad than before",
                source: {
                    pointer: "/price/currency"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "a bad thing",
                source: {
                    pointer: "/a_list/0/thingy"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "bar",
                source: {
                    pointer: "/a_list/0/foo"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "another bad thing",
                source: {
                    pointer: "/a_list/1/thingy"
                }
            },
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "bar",
                source: {
                    pointer: "/a_list/1/foo"
                }
            },    
            {
                status: "400",
                code: "invalid",
                title: "Bad Request",
                detail: "bat",
                source: {
                    pointer: "/a_list/1/ding"
                }
            }
        ]
    }
    """
    raise exceptions.ValidationError(
        {
            "bad": ["this field is bad 1", "this field is bad 2"],
            "price": {"amount": "this field is also bad", "currency": "bad, but less bad than before"},
            "a_list": [
                {"thingy": "a bad thing", "foo": "bar"},
                {"thingy": "another bad thing", "foo": "bar", "ding": "bat"},
            ],
        }
    )
