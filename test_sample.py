"""
Sample tests to demonstrate the bisection feature.
"""
import pytest
import sys


def test_always_passes():
    """A test that should always pass."""
    assert 1 + 1 == 2


def test_python_version_dependent():
    """A test that might fail depending on Python version."""
    # This will fail if we're running Python < 3.10
    assert sys.version_info >= (3, 8), f"Python version {sys.version_info} is too old"


def test_package_dependent():
    """A test that depends on package versions."""
    try:
        import numpy as np
        # This might fail with different numpy versions
        assert hasattr(np, 'ndarray'), "numpy should have ndarray"
        # Create a simple array test
        arr = np.array([1, 2, 3])
        assert arr.sum() == 6
    except ImportError:
        pytest.skip("numpy not available")


def test_sometimes_fails():
    """A test that we can toggle to demonstrate bisection."""
    # We can change this to False to simulate a failing test
    SHOULD_PASS = False  # Changed to False to demonstrate bisection
    assert SHOULD_PASS, "This test was configured to fail"


def test_import_specific_feature():
    """Test that depends on specific library features."""
    try:
        import json
        # Test a feature that should be available
        data = {"test": "value"}
        assert json.dumps(data) == '{"test": "value"}'
    except ImportError:
        pytest.fail("json module should be available")


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_parametrized(value):
    """Parametrized test to show multiple test nodeids."""
    assert value > 0
    # We can make some parameter values fail
    if value == 4:
        # Uncomment to make this parameter fail
        assert False, f"Parameter {value} configured to fail"