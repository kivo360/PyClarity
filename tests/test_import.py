"""Test pyclarity."""

import pyclarity


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(pyclarity.__name__, str)
