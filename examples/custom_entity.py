from mcstructure import Block, Structure
import nbtx
from pathlib import Path

here = Path(__file__).parent

struct = Structure((2, 2, 2), Block("minecraft:air"))

struct.add_entity(
    nbtx.TagCompound(
        "",
        [
            nbtx.TagList(
                "Armor",
                child_id=nbtx.TagCompound.id(),
                value=[
                    # head slot
                    nbtx.TagCompound(
                        "",
                        [
                            nbtx.TagCompound("Block", [
                                nbtx.TagString("name", "minecraft:player_head"),
                                nbtx.TagCompound("states", [
                                    nbtx.TagInt("facing_direction", 0),
                                ]),
                                nbtx.TagInt("version", 18168865),
                            ]),
                            nbtx.TagByte("Count", 1),
                            nbtx.TagShort("Damage", 0),
                            nbtx.TagString("Name", "minecraft:player_head"),
                            nbtx.TagByte("WasPickedUp", 0),
                        ]
                    ),

                    # chest slot
                    nbtx.TagCompound(
                        "",
                        [
                            nbtx.TagByte("Count", 0),
                            nbtx.TagShort("Damage", 0),
                            nbtx.TagString("Name", ""),
                            nbtx.TagByte("WasPickedUp", 0),
                        ]
                    ),

                    # legs slot
                    nbtx.TagCompound(
                        "",
                        [
                            nbtx.TagByte("Count", 0),
                            nbtx.TagShort("Damage", 0),
                            nbtx.TagString("Name", ""),
                            nbtx.TagByte("WasPickedUp", 0),
                        ]
                    ),

                    # feet slot
                    nbtx.TagCompound(
                        "",
                        [
                            nbtx.TagByte("Count", 0),
                            nbtx.TagShort("Damage", 0),
                            nbtx.TagString("Name", ""),
                            nbtx.TagByte("WasPickedUp", 0),
                        ]
                    ),
                ]
            ),
            nbtx.TagList(
                "Attributes",
                child_id=nbtx.TagCompound.id(),
                value=[]
            ),
            nbtx.TagList(
                "Pos",
                child_id=nbtx.TagFloat.id(),
                value=[
                    nbtx.TagFloat("", 0),
                    nbtx.TagFloat("", 0),
                    nbtx.TagFloat("", 0),
                ]
            ),
            nbtx.TagList(
                "Rotation",
                child_id=nbtx.TagFloat.id(),
                value=[
                    nbtx.TagFloat("", -90.),
                    nbtx.TagFloat("", 0.),
                ]
            ),
            nbtx.TagList(
                "definitions",
                child_id=nbtx.TagString.id(),
                value=[
                    nbtx.TagString("", "+minecraft:armor_stand"),
                ]
            ),
            nbtx.TagString("identifier", "minecraft:armor_stand"),
        ]
    )
)

with here.joinpath("out/custom_entity.mcstructure").open("wb") as f:
    struct.dump(f)
