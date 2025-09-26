"""
Sample tests to demonstrate the bisection feature with numpy version dependency.
"""
import pytest
import sys


def test_always_passes():
    """A test that should always pass."""
    assert 1 + 1 == 2


def test_numpy_version_dependent():
    """A test that depends on numpy version - will fail if numpy >= 2.2."""
    try:
        import numpy as np
        print(f"numpy version: {np.__version__}")

        # This test expects numpy < 2.2
        # It will pass with numpy 2.1.0 but fail with 2.2+
        major, minor = map(int, np.__version__.split('.')[:2])
        version_tuple = (major, minor)

        assert version_tuple < (2, 2), f"This test expects numpy < 2.2, got {np.__version__}"

    except ImportError:
        pytest.fail("numpy should be available")


def test_numpy_basic_functionality():
    """Test basic numpy functionality."""
    try:
        import numpy as np

        # Basic array operations that should work in any version
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.sum() == 15
        assert arr.mean() == 3.0
        assert len(arr) == 5

    except ImportError:
        pytest.fail("numpy should be available")


def test_numpy_api_compatibility():
    """Test that specific numpy APIs are available - version dependent."""
    try:
        import numpy as np

        # This test will be sensitive to numpy version changes
        arr = np.array([1.0, 2.0, 3.0])

        # Test that basic functions exist
        assert hasattr(np, 'ndarray')
        assert hasattr(np, 'array')
        assert hasattr(np, 'zeros')

        # Create different array types
        zeros = np.zeros(3)
        ones = np.ones(3)

        assert zeros.sum() == 0
        assert ones.sum() == 3

    except ImportError:
        pytest.fail("numpy should be available")