"""pyll_json_errors.transform"""
from unittest import mock

from pyll_json_errors import models, transform


class TestTransform(transform.BaseTransform):
    def make_json_errors(self, sources):
        return [models.JsonError(title=value) for value in sources]


def test_BaseTransform__to_list():
    """Test transform class returns a list of JsonError objects."""
    ttf = TestTransform()
    ttf.make_json_errors = mock.MagicMock()
    ttf.to_list(sources=["foo", "bar"])

    ttf.make_json_errors.assert_called_once()


def test_BaseTransform__to_array():
    """Test transform class returns a JsonErrorArray object."""
    ttf = TestTransform()
    result = ttf.to_array(sources=["foo", "bar"])

    assert isinstance(result, models.JsonErrorArray)
    assert len(result.errors) == 2
