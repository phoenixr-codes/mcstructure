"""
Read and write Minecraft .mcstructure files.
"""

# TODO: coordinates might be in wrong order (XYZ -> ZYX)
# TODO: second layer (waterlogged blocks)
# TODO: additional block data
# TODO: entities

from __future__ import annotations

from dataclasses import dataclass
from itertools import repeat
import json
from typing import Any, BinaryIO, NoReturn, Optional

import numpy as np
from numpy.typing import NDArray
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String

Coordinate = tuple[int, int, int]


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
    
    if isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res
    
    if isinstance(tag, BaseTag):
        return tag.value
    
    return tag

def _into_tag(obj: Any) -> BaseTag:
    """
    Turn a python tree into an NBT tree.
    """
    if isinstance(obj, int):
        return TAG_Int(obj)
    
    if isinstance(obj, str):
        return TAG_String(obj)
    
    return obj

def is_valid_structure_name(name: str, with_prefix: bool = False) -> bool:
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

@dataclass(init = False)
class Block:
    """
    Attributes
    ----------
    name
        The name of the block.
    
    states
        The states of the block.
    
    Example
    -------
    Block("minecraft:wool", color = "red")
    """
    identifier: str
    states: dict[str, Any]
    
    def __init__(self, identifier: str, **states: Any):
        self.identifier = identifier
        self.states = states
    
    def get_namespace_and_name(self) -> tuple[Optional[str], str]:
        if ":" in self.identifier:
            ns, name = self.identifier.split(":", 1)
            return ns, name
        
        return (None, self.identifier)
    
    def get_name(self) -> str:
        return self.get_namespace_and_name()[1]
    
    def get_namespace(self) -> Optional[str]:
        return self.get_namespace_and_name()[0]

class Structure:
    """
    Attributes
    ----------
    size
        The size of the structure.
    """
    def __init__(
        self,
        size: tuple[int, int, int],
        fill: Optional[Block] = Block("minecraft:air")
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
            is filled with structure void blocks.
        """
        self._structure: NDArray[np.intc]
        
        self._size = size
        self._palette: list[Block] = []
        
        if fill is None:
            self._structure = np.full(size, -1, dtype = np.intc)
        
        else:
            self._structure = np.zeros(size, dtype = np.intc)
            self._palette.append(fill)
    
    @classmethod
    def load(cls, file: BinaryIO):
        """
        Loads an mcstructure file.
        
        Parameters
        ----------
        file
            File object to read.
        """
        nbt = NBTFile(file, little_endian = True)
        size: tuple[int, int, int] = tuple(x.value for x in nbt["size"]) # type: ignore
        
        struct = cls(size)
        
        struct._structure = np.array(
            [_into_pyobj(x) for x in nbt["structure"]["block_indices"][0]],
            dtype = np.intc
        ).reshape(size)
        
        struct._palette.extend([
            Block(block["name"].value, **_into_pyobj(block["states"].value))
            for block in nbt["structure"]["palette"]["default"]["block_palette"]
        ])
        
        return struct
    
    @property
    def size(self) -> tuple[int, int, int]:
        return self._size
    
    def __repr__(self) -> str:
        return repr(self._get_str_array())
    
    def __str__(self) -> str:
        return str(self._get_str_array())
    
    def _get_str_array(
        self,
        with_namespace: bool = False,
        with_states: bool = False
    ) -> NDArray[str]:
        def stringify(block: Block) -> str:
            name = ""
            
            if with_namespace and (ns := block.get_namespace()) is not None:
                name += ns + ":"
            
            name += block.get_name()
            
            if with_states:
                name += f" [{json.dumps(block.states)[1:-1]}]"
            
            return name
        
        arr = self.get_structure().copy()
        vec = np.vectorize(stringify)
        return vec(arr)
    
    def _add_block_to_palette(self, block: Optional[Block]) -> int:
        if block is None:
            return -1
        
        if block in self._palette:
            return self._palette.index(block)
        
        self._palette.append(block)
        return len(self._palette) - 1
    
    def get_structure(self) -> NDArray[Block]:
        """
        Returns the structure as a numpy array filled
        with the corresponding block objects.
        """
        arr = np.empty(self._structure.shape, dtype = object)
        for key, block in enumerate(self._palette):
            arr[self._structure == key] = block
        return arr
    
    def dump(self, file: BinaryIO) -> None:
        """
        Serialize the structure as a mcstructure.
        
        Parameters
        ----------
        file
            File object to write to.
        """
        nbt = NBTFile(value = dict(
            format_version = TAG_Int(1),
            size = TAG_List(TAG_Int, map(TAG_Int, self._size)),
            
            structure = TAG_Compound(dict(
                block_indices = TAG_List(TAG_List, [
                    TAG_List(TAG_Int, map(TAG_Int, self._structure.flatten())),
                    TAG_List(TAG_Int, map(TAG_Int, repeat(-1, self._structure.size)))
                ]),
                entities = TAG_List(TAG_Compound, []),
                palette = TAG_Compound(dict(
                    default = TAG_Compound(dict(
                        block_palette = TAG_List(TAG_Compound, [
                            TAG_Compound({
                                "name": TAG_String(block.identifier),
                                "states": TAG_Compound({
                                    state_name: _into_tag(state_value)
                                    for state_name, state_value in block.states.items()
                                }),
                                "version": TAG_Int(COMPABILITY_VERSION)
                            })
                        for block in self._palette]),
                        block_position_data = TAG_Compound({})
                    ))
                ))
            )),
            structure_world_origin = TAG_List(TAG_Int, [0, 0, 0])
        ), little_endian = True)
        nbt.save(file, little_endian = True)
    
    def get_block(
        self,
        coordinate: Coordinate
    ) -> Optional[Block]:
        """
        Parameters
        ----------
        coordinate
            The coordinte of the block.
        """
        x, y, z = coordinate
        return self._palette[self._structure[x, y, z]]
    
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
            structure void will be used.
        """
        x, y, z = coordinate
        
        ident = self._add_block_to_palette(block)
        
        self._structure[x, y, z] = ident
        return self
    
    def set_blocks(
        self,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        block: Block,
    ) -> Structure:
        fx, fy, fz = from_coordinate
        tx, ty, tz = to_coordinate
        
        ident = self._add_block_to_palette(block)
        
        self._structure[fx:tx, fy:ty, fz:tz]
        return self


if __name__ == '__main__':
    struct = Structure((10, 10, 10), Block("minecraft:wool", color = "white"))
    print(struct)
