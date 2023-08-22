from mcstructure import has_suitable_size, STRUCTURE_MAX_SIZE


def test_oversized() -> None:
    assert has_suitable_size(STRUCTURE_MAX_SIZE)
    assert not has_suitable_size((65, 0, 0))
