from mcstructure import has_suitable_size, STRUCTURE_MAX_SIZE, Structure, Block
import pytest


def test_oversized() -> None:
    assert has_suitable_size(STRUCTURE_MAX_SIZE)
    assert not has_suitable_size((65, 0, 0))

def test_resize_larger() -> None:
    dirt = Block("minecraft:dirt")
    air = Block("minecraft:air")
    struct = Structure((2, 2, 2), fill=dirt)
    struct.resize((4, 4, 4), air)
    assert struct.get_block((3, 3, 3)) == air
    assert struct.get_block((0, 0, 0)) == dirt
    assert struct.get_block((1, 1, 1)) == dirt
    assert struct.get_block((2, 2, 2)) == air

def test_resize_smaller() -> None:
    dirt = Block("minecraft:dirt")
    air = Block("minecraft:air")
    struct = Structure((4, 4, 4), fill=air)
    struct.resize((2, 2, 2))
    with pytest.raises(IndexError):
        assert struct.get_block((3, 3, 3)) is None
    with pytest.raises(IndexError):
        assert struct.get_block((2, 2, 2)) is None
    assert struct.get_block((1, 1, 1)) == dirt
    assert struct.get_block((0, 0, 0)) == dirt
