Quickstart
==========

pyll_json_errors is broken into two primary pieces:

* | Model classes to represent JSON API error objects, located in the :code:`pyll_json_errors.models`
    sub-module.
* | Helper classes to transform those models into HTTP responses, located in the
    :code:`pyll_json_errors.contrib` sub-module.

Model Classes
-------------

At a basic level, :code:`pyll_json_errors.models.JsonError` objects should be created, fed into
:code:`pyll_json_errors.models.JsonErrorArray`, then serialized with :code:`.serialized()`.

Example:

.. code-block:: python

    from pyll_json_errors import models

    err_one = models.JsonError(
        id="someId",
        status=400,
        code="custom-code-XXX",
        title="Validation Error",
        detail="'leaflink.com' is not a valid email domain.",
        source=models.JsonErrorSourcePointer(keys=("user", "email"))
    )
    err_two = models.JsonError(
        status="401",
        title="Unauthorized",
        detail="You do not have access to LeafLink email domains."
    )

    array = models.JsonErrorArray([err_one, err_two])

    # array.status
    # 400

    # array.serialized()
    # {"errors": [{"id": "someId", "status": "400", "code": "custom-code-XXX", "title": "Validation Error", "detail": "'leaflink.com' is not a valid email domain.", "source": {"pointer": "/user/email"}}, {"status": "401", "title": "Unauthorized", "detail": "You do not have access to LeafLink email domains."}]}
