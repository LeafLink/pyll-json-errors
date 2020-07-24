"""pyll_json_errors.__init__"""
import pytest

import pyll_json_errors


@pytest.mark.parametrize("package, raises", [("the_package_does_not_exist", True), ("os", False)])
def test__check_dependency(package, raises):
    """Test checking for deps."""
    if raises:
        with pytest.raises(ModuleNotFoundError):
            pyll_json_errors._check_dependency(package, __name__)
    else:
        pyll_json_errors._check_dependency(package, __name__)


def test_version():
    assert pyll_json_errors.__version__ == "0.1.0"
