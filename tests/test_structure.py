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
    struct = Structure((4, 4, 4), fill=dirt)
    struct.resize((2, 2, 2))
    with pytest.raises(IndexError):
        assert struct.get_block((3, 3, 3)) is None
    with pytest.raises(IndexError):
        assert struct.get_block((2, 2, 2)) is None
    assert struct.get_block((1, 1, 1)) == dirt
    assert struct.get_block((0, 0, 0)) == dirt


def test_combine() -> None:
    dirt = Block("minecraft:dirt")
    air = Block("minecraft:air")
    void = Block("minecraft:structure_void")
    struct_a = Structure((1, 2, 2), fill=air)
    struct_b = Structure((1, 2, 2), fill=dirt)
    struct_c = struct_a.combine(struct_b, (0, 1, 1))

    # Check the combined structure
    assert struct_c.get_block((0, 0, 0)) == air
    assert struct_c.get_block((0, 0, 1)) == air
    assert struct_c.get_block((0, 0, 2)) == void
    assert struct_c.get_block((0, 1, 0)) == air
    assert struct_c.get_block((0, 1, 1)) == dirt
    assert struct_c.get_block((0, 1, 2)) == dirt
    assert struct_c.get_block((0, 2, 0)) == void
    assert struct_c.get_block((0, 2, 1)) == dirt
    assert struct_c.get_block((0, 2, 2)) == dirt
