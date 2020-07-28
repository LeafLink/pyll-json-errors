"""pyll_json_errors.utils"""
import pytest

from pyll_json_errors import utils


@pytest.mark.parametrize(
    "inp, outp",
    [
        (
            {"one": 1, "two": [2, 2], "three": {"three_one": 31, "three_two": {"0": 320, "1": 321, "2": {"four": 4}}}},
            {
                ("one",): 1,
                ("two", "0"): 2,
                ("two", "1"): 2,
                ("three", "three_one"): 31,
                ("three", "three_two", "0"): 320,
                ("three", "three_two", "1"): 321,
                ("three", "three_two", "2", "four"): 4,
            },
        ),
        (
            {0: {"email": "Not Valid"}, 1: {"name": "What is a name?"}},
            {("0", "email"): "Not Valid", ("1", "name"): "What is a name?"},
        ),
    ],
)
def test__flatten_dict(inp, outp):
    """Test flatten dicts results in expected keys."""
    assert utils.flatten_dict(data=inp) == outp
