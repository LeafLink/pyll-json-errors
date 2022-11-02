Installation
============

Python Version
--------------

Pyll JSON Error supports python 3.8 and higher.

Install Instructions
--------------------

Currently, :code:`pyll_json_errors` is only installable from GitHub.

Poetry Install
^^^^^^^^^^^^^^

.. code-block:: bash

    # Install stable
    poetry add "git+https://github.com/LeafLink/pyll-json-errors.git@main"

    # Install specific version
    poetry add "git+https://github.com/LeafLink/pyll-json-errors.git@X.Y.Z"

    # Install with optional dependency
    poetry add "git+https://github.com/LeafLink/pyll-json-errors.git@main" -E all

Pip Install
^^^^^^^^^^^

.. code-block:: bash

    # Install stable
    pip3 install "pyll-json-errors @ git+https://github.com/LeafLink/pyll-json-errors.git"

    # Install specific version
    pip3 install "pyll-json-errors @ git+https://github.com/LeafLink/pyll-json-errors.git@X.Y.Z"

    # Install with optional dependency
    pip3 install "pyll-json-errors[all] @ git+https://github.com/LeafLink/pyll-json-errors.git"

Uninstall Instructions
----------------------

Poetry Uninstall
^^^^^^^^^^^^^^^^

.. code-block:: bash

    poetry remove pyll-json-errors

Pip Uninstall
^^^^^^^^^^^^^

.. code-block:: bash

    pip3 uninstall pyll-json-errors


Optional Dependencies
---------------------

Pyll JSON Errors comes with various optional dependencies. Thes dependencies are required to using the respective
modules in :mod:`pyll_json_errors.contrib`.

* :code:`rest_framework`: Django REST Framework dependencies.
* :code:`flask`: Flask dependencies.
* :code:`marshmallow`: Marshmallow dependencies.
* :code:`all`: All dependencies.

If you're integrating into an existing project which already has the dependencies you need, just install without any
optionals.
