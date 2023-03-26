"""
Read and write Minecraft .mcstructure files.
"""

# TODO: coordinates might be in wrong order (XYZ -> ZYX)
# TODO: make Structure._structure public
# TODO: test mirror
# TODO: test rotate
# TODO: second layer (waterlogged blocks)
# TODO: entities
# TODO: export as 3d model (might be extension)

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from itertools import repeat
import json
from typing import Any, BinaryIO, Optional, Tuple, Union, Dict

import numpy as np
from numpy.typing import NDArray
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String, TAG_Byte  # type: ignore

Coordinate = Tuple[int, int, int]

# Compatibility versioning number for blocks in 1.19.
COMPABILITY_VERSION: int = 17959425


def _into_pyobj(tag: BaseTag) -> Any:
    """
    Turns an NBT tree into a python tree.
    """
    if isinstance(tag, (TAG_Compound, dict)):
        res = {}
        for key, value in tag.items():
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res[key] = value
        return res

    elif isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res

    elif isinstance(tag, BaseTag):
        return tag.value

    return tag


def _into_tag(obj: Any) -> BaseTag:
    """
    Turn a python tree into an NBT tree.
    """
    if isinstance(obj, (TAG_Compound, dict)):
        res = {}
        for key, value in obj.items():
            if not isinstance(value, BaseTag):
                value = _into_tag(value)
            res[key] = value
        return TAG_Compound(res)

    elif isinstance(obj, (TAG_List, list)):
        res = []
        for value in obj:
            if not isinstance(value, BaseTag):
                value = _into_tag(value)
            res.append(value)
        return TAG_List(
            tag_type=(type(_into_tag(obj[0])) if obj else TAG_String), value=res
        )

    elif isinstance(obj, int):
        return TAG_Int(obj)

    elif isinstance(obj, str):
        return TAG_String(obj)

    return obj


def is_valid_structure_name(name: str, *, with_prefix: bool = False) -> bool:
    """
    Validates the structure name.

    .. seealso: https://minecraft.fandom.com/wiki/Structure_Block

    Parameters
    ----------
    name
        The name of the structure.

    with_prefix
        Whether to take the prefix (e.g. ``mystructure:``)
        into account.
    """
    if with_prefix:
        name = name.replace(":", "", 1)

    return all((char.isalnum() and char in "-_") for char in name)


@dataclass(init=False)
class Block:
    """
    Attributes
    ----------
    base_name
        The name of the block.

    states
        The states of the block.

    Example
    -------
    .. code-block::

        Block("minecraft:wool", color = "red")
    """

    namespace: str
    base_name: str
    states: dict[str, Union[int, str, bool]]
    extra_data: dict[str, Union[int, str, bool]]

    def __init__(
            self,
            namespace: str,
            base_name: str,
            states: dict[str, Union[int, str, bool]] = {},
            extra_data: dict[str, Union[int, str, bool]] = {},
            compability_version: int = COMPABILITY_VERSION,
    ):
        """
        Parameters
        ----------
        namespace
            The namespace of the block (e.g. "minecraft").
        base_name
            The name of the block (e.g. "air").

        states
            The block states such as {'color': 'white'} or {"stone_type":1}.
            This varies by every block.

        extra_data
            [Optional] The additional data of the block.

        compability_version
            [Optional] The compability version of the block, now(1.19) is 17959425
        """
        self.namespace = namespace
        self.base_name = base_name
        self.states = states
        self.extra_data = extra_data
        self.compability_version = compability_version

    @classmethod
    def from_identifier(
            cls,
            identifier: str,
            compability_version=COMPABILITY_VERSION,
            **states: Union[int, str, bool],
    ):
        """
        Parameters
        ----------
        identifier
            The identifier of the block (e.g. "minecraft:wool").

        states
            The block states such as "color" or "stone_type".
            This varies by every block.

        compability_version
            It's not written here.
        """

        if ":" in identifier:
            namespace, base_name = identifier.split(":", 1)
        else:
            namespace = "minecraft"
            base_name = identifier

        block = cls(
            namespace, base_name, states, compability_version=compability_version
        )

        return block

    def __str__(self) -> str:
        return self.stringify()

    def __dict__(self) -> dict:
        return self.dictionarify()

    def add_states(
            self,
            states: dict[str, Union[int, str, bool]],
    ) -> None:
        self.states.update(states)

    def add_extra_data(
            self,
            extra_data: dict[str, Union[int, str, bool]],
    ) -> None:
        self.extra_data.update(extra_data)

    def dictionarify(self, *, with_states: bool = True) -> Dict[str, Any]:
        result = {
            "name": self.identifier,
            "states": self.states if with_states else {},
            "version": self.compability_version,
        }

        return result

    def dictionarify_with_block_entity(
            self, *, with_states: bool = True
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        result = {
            "name": self.identifier,
            "states": self.states if with_states else {},
            "version": self.compability_version,
        }

        return result, self.extra_data

    def stringify(
            self,
            *,
            with_namespace: bool = True,
            with_states: bool = True,
    ) -> str:
        result = ""
        if with_namespace:
            result += self.namespace + ":"
        result += self.get_name()
        if with_states:
            result += f" [{json.dumps(self.states)[1:-1]}]"
        return result

    def get_namespace_and_name(self) -> tuple[str, str]:
        """
        Returns the namespace and the name of the block.
        """
        return self.namespace, self.base_name

    def get_identifier(self) -> str:
        """
        Returns the identifier of the block.
        """
        return self.namespace + ":" + self.base_name

    def get_name(self) -> str:
        """
        Returns the name of the block.
        """
        return self.base_name

    def get_namespace(self) -> Optional[str]:
        """
        Returns the namespace of the block.
        """
        return self.namespace

    @property
    def identifier(self) -> str:
        """
        The identifier of the block.
        """
        return self.get_identifier()


class Structure:
    """
    Class representing a Minecraft structure that
    consists of blocks and entities.

    Attributes
    ----------
    _size
        The size of the structure.
    """

    structure_indecis: NDArray[np.intc]

    def __init__(
            self,
            size: tuple[int, int, int],
            fill: Optional[Block] = None,
            compability_version: int = COMPABILITY_VERSION,
    ):
        """
        Parameters
        ----------
        size
            The size of the structure.

        fill
            Fill the structure with this block at
            creation of a new structure object.

            If this is set to ``None`` the structure
            is filled with "Structure Void" blocks.

            "minecraft:air" is used as default.
        """
        self.structure_indecis: NDArray[np.intc]

        self._size = size
        self._palette: list[Block] = []
        self._special_block_indices: list[int] = []

        if fill is None:
            self.structure_indecis = np.full(size, -1, dtype=np.intc)

        else:
            self.structure_indecis = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)

        self.compability_version = compability_version

    @classmethod
    def load(cls, file: BinaryIO):
        """
        Loads an mcstructure file.

        Parameters
        ----------
        file
            File object to read.
        """
        nbt = NBTFile(file, little_endian=True)
        size: tuple[int, int, int] = tuple(x.value for x in nbt["size"])  # type: ignore

        struct = cls(size)

        # see https://wiki.bedrock.dev/nbt/mcstructure.html
        # of a .mcstructure file's NBT format
        # while Chinese developers could see my translation at
        # ../docs/mcstructure%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84.md

        struct.structure_indecis = np.array(
            [_into_pyobj(x) for x in nbt["structure"]["block_indices"][0]],
            dtype=np.intc,
        ).reshape(size)

        struct._palette.extend(
            [
                Block.from_identifier(
                    block["name"].value,
                    **_into_pyobj(block["states"].value),
                    compability_version=_into_pyobj(block["version"]),
                )
                for block in nbt["structure"]["palette"]["default"]["block_palette"]
            ]
        )

        for block_index, block_eneity_data in nbt["structure"]["palette"]["default"][
            "block_position_data"
        ].items():
            struct._palette[int(block_index)].add_extra_data(
                _into_pyobj(block_eneity_data)
            )
            struct._special_block_indices.append(int(block_index))

        return struct

    @property
    def size(self) -> tuple[int, int, int]:
        return self._size

    def __repr__(self) -> str:
        return repr(self._get_str_array())

    def __str__(self) -> str:
        return str(self._get_str_array())

    def _get_str_array(
            self, *, with_namespace: bool = False, with_states: bool = False
    ) -> NDArray[Any]:
        """
        Returns a numpy array where each entry is a
        readable string of the corresponding block.

        Parameters
        ----------
        with_namespace
            Adds the namespace to the string if present.

        with_states
            Adds the block states to the string if present.
        """
        arr = self.get_structure().copy()
        vec = np.vectorize(
            partial(
                Block.stringify, with_namespace=with_namespace, with_states=with_states
            )
        )
        return vec(arr)

    def _add_block_to_palette(self, block: Optional[Block]) -> int:
        """
        Adds a block to the palette.

        Parameters
        ----------
        block
            The block to add. If this is set to ``None``
            "Structure Void" will be used.

        Returns
        -------
        The position of the block in the palette. This is
        ``-1`` when ``None`` is used as ``block``.
        """
        if block is None:
            return -1

        if block in self._palette:
            return self._palette.index(block)

        self._palette.append(block)
        return len(self._palette) - 1

    def get_structure(self) -> NDArray[Any]:
        """
        Returns the structure as a numpy array filled
        with the corresponding `Block` objects.
        """
        arr = np.full(
            self.structure_indecis.shape,
            Block(
                "minecraft",
                "structure_void",
                compability_version=self.compability_version,
            ),
            dtype=object,
        )
        for key, block in enumerate(self._palette):
            arr[self.structure_indecis == key] = block
        return arr

    def dump(self, file: BinaryIO) -> None:
        """
        Serialize the structure as a ``mcstructure``.

        Parameters
        ----------
        file
            File object to write to.
        """
        nbt = NBTFile(
            value=dict(
                format_version=TAG_Int(1),
                size=TAG_List(TAG_Int, map(TAG_Int, self._size)),
                structure=TAG_Compound(
                    dict(
                        block_indices=TAG_List(
                            TAG_List,
                            [
                                TAG_List(
                                    TAG_Int,
                                    map(TAG_Int, self.structure_indecis.flatten()),
                                ),
                                TAG_List(
                                    TAG_Int,
                                    map(
                                        TAG_Int, repeat(-1, self.structure_indecis.size)
                                    ),
                                ),
                            ],
                        ),
                        entities=TAG_List(TAG_Compound, []),
                        palette=TAG_Compound(
                            dict(
                                default=TAG_Compound(
                                    dict(
                                        block_palette=TAG_List(
                                            TAG_Compound,
                                            [
                                                TAG_Compound(
                                                    dict(
                                                        name=TAG_String(
                                                            block.identifier
                                                        ),
                                                        states=TAG_Compound(
                                                            {
                                                                state_name: _into_tag(
                                                                    state_value
                                                                )
                                                                for state_name, state_value in block.states.items()
                                                            }
                                                        ),
                                                        version=TAG_Int(
                                                            block.compability_version
                                                        ),
                                                    )
                                                )
                                                for block in self._palette
                                            ],
                                        ),
                                        block_position_data=TAG_Compound(
                                            dict(
                                                [
                                                    (
                                                        str(block_index),
                                                        _into_tag(
                                                            self._palette[
                                                                block_index
                                                            ].extra_data
                                                        ),
                                                    )
                                                    for block_index in self._special_block_indices
                                                ]
                                            )
                                        ),
                                    )
                                )
                            )
                        ),
                    )
                ),
                structure_world_origin=TAG_List(TAG_Int, [0, 0, 0]),
            ),
            little_endian=True,
        )
        nbt.save(file, little_endian=True)

    def mirror(self, axis: str) -> Structure:
        """
        Flips the structure.

        Parameters
        ----------
        axis
            Turn the structure either the ``X`` or ``Z`` axis.
            Use ``"X"``, ``"x"``,``"Z"`` or ``"z"``.
        """
        if axis in "Xx":
            self.structure_indecis = self.structure_indecis[::-1, :, :]
        elif axis in "Zz":
            self.structure_indecis = self.structure_indecis[:, :, ::-1]
        else:
            raise ValueError(f"invalid argument for 'rotation' ({axis!r})")
        return self

    def rotate(self, by: int) -> Structure:
        """
        Rotates the structure.

        Parameters
        ----------
        by
            Rotates the structure by ``90``, ``180``
            or ``270`` degrees.
        """
        if by == 90:
            self.structure_indecis = np.rot90(self.structure_indecis, k=1, axes=(0, 1))
        elif by == 180:
            self.structure_indecis = np.rot90(self.structure_indecis, k=2, axes=(0, 1))
        elif by == 270:
            self.structure_indecis = np.rot90(self.structure_indecis, k=3, axes=(0, 1))
        else:
            raise ValueError(f"invalid argument for 'by' ({by!r})")
        return self

    def get_block(self, coordinate: Coordinate) -> Optional[Block]:
        """
        Returns the block in a specific position.

        Parameters
        ----------
        coordinate
            The coordinte of the block.
        """
        x, y, z = coordinate
        return self._palette[self.structure_indecis[x, y, z]]

    def set_block(
            self,
            coordinate: Coordinate,
            block: Optional[Block],
    ) -> Structure:
        """
        Puts a block into the structure.

        Parameters
        ----------
        coordinate
            Relative coordinates of the block's position.

        block
            The block to place. If this is set to ``None``
            "Structure Void" blocks will be used.
        """
        x, y, z = coordinate

        ident = self._add_block_to_palette(block)
        if block.extra_data:
            self._special_block_indices.append(ident)

        self.structure_indecis[x, y, z] = ident
        return self

    def fill_blocks(
            self,
            from_coordinate: Coordinate,
            to_coordinate: Coordinate,
            block: Block,
    ) -> Structure:
        """
        Puts multiple blocks into the structure.

        Notes
        -----
        Both start and end points are filled.

        Parameters
        ----------
        from_coordinate
            Relative coordinates of the start corner.

        to_coordinate
            Relative coordinates of the end corner.

        block
            The block to place. If this is set to ``None``
            "STructure Void" blocks will be used to fill.
        """
        fx, fy, fz = from_coordinate
        tx, ty, tz = to_coordinate

        ident = self._add_block_to_palette(block)
        if block.extra_data:
            self._special_block_indices.append(ident)
        # print([[[ident for k in range(abs(fz-tz)+1) ]for j in range(abs(fy-ty)+1)]for i in range(abs(fx-tx)+1)])
        self.structure_indecis[fx: tx + 1, fy: ty + 1, fz: tz + 1] = np.array(
            [
                [
                    [ident for k in range(abs(fz - tz) + 1)]
                    for j in range(abs(fy - ty) + 1)
                ]
                for i in range(abs(fx - tx) + 1)
            ],
            dtype=np.intc,
        ).reshape([abs(i) + 1 for i in (fx - tx, fy - ty, fz - tz)])
        return self
