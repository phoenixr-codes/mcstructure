from mcstructure import Structure, STRUCTURE_MAX_SIZE
import pytest


def test_oversized() -> None:
    Structure(STRUCTURE_MAX_SIZE)
    with pytest.raises(ValueError):
        Structure((65, 0, 0))
