import random

import pytest

from .. import encode, decode


current_limit = 42343030

random.seed(0)
test_numbers = [random.randint(0, current_limit - 1)
                for _ in range(20)]

roundtrip_cases = pytest.mark.parametrize('n',
      [0, 1, 2, 3, 25161700, current_limit - 1] + test_numbers)

@roundtrip_cases
def test_roundtrip_3(n):
    # TODO: Parametrize n_words too.
    namehash = encode(n, n_words=3)
    actual = decode(namehash)
    assert n == actual


@pytest.mark.parametrize('n', [-1, current_limit])
def test_overflow_3(n):
    with pytest.raises(OverflowError):
        encode(n, n_words=3)


current_limit = 1567225352

@pytest.mark.parametrize('n',
     [0, 1, 2, 3, current_limit - 1] +
     [random.randint(0, current_limit - 1) for _ in range(20)])
def test_roundtrip_4(n):
    namehash = encode(n, n_words=4)
    assert len(namehash.split('-')) == 4
    actual = decode(namehash)
    assert n == actual


@pytest.mark.parametrize('n', [-1, current_limit])
def test_overflow_4(n):
    with pytest.raises(OverflowError):
        encode(n, n_words=4)
