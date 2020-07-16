from django.http.response import Http404
from rest_framework import decorators, exceptions


@decorators.api_view(["GET"])
def error_403(request):
    raise exceptions.PermissionDenied()


@decorators.api_view(["GET"])
def error_404(request):
    raise exceptions.NotFound()


@decorators.api_view(["GET"])
def error_404_django(request):
    raise Http404()


@decorators.api_view(["GET"])
def error_500(request):
    raise RuntimeError("an error")


@decorators.api_view(["GET"])
def error_400(request):
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
