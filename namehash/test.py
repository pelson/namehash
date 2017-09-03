from .namehash import encode, decode
import pytest


roundtrip_cases = pytest.mark.parametrize('n', [0, 1, 2, 3, ])

@roundtrip_cases
def test_roundtrip(n):
    namehash = encode(n, 3)
    actual = decode(namehash)
    assert n == actual
