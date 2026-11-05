import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from result import calculate_result


@pytest.mark.parametrize(
    "marks, total, percentage, grade, status",
    [
        pytest.param(100, 100, 100.0, "A", "PASS", id="full-marks"),
        pytest.param(0, 100, 0.0, "F", "FAIL", id="zero-marks"),
        pytest.param(45, 100, 45.0, "C", "PASS", id="partial-marks"),
        pytest.param(150, 100, None, None, "INVALID", id="invalid-input"),
    ],
)
def test_calculate_result(marks, total, percentage, grade, status):
    result = calculate_result(marks, total)

    assert result["percentage"] == percentage
    assert result["grade"] == grade
    assert result["status"] == status
