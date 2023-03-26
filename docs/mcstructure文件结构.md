
**此文档译自https://wiki.bedrock.dev/nbt/mcstructure.html**

# `.MCSTRUCTURE`文件结构

mcstructure 文件是未经压缩的 [NBT 文件](https://wiki.vg/NBT#Specification)，也正如《我的世界：基岩版》的所有 NBT 文件一样，其皆以小端字节序（又称小端序）存储。以下是此类文件的 NBT 标签结构：

<!-- <style>img{width: 16px;}</style> -->

[nbt-tag-types]: https://static.wikia.nocookie.net/minecraft_zh_gamepedia/images/d/d0/Nbtsheet.png/revision/latest
[int]: https://foruda.gitee.com/images/1678607417066876136/a1771588_9911226.png?width=16
[string]: https://foruda.gitee.com/images/1678607425650690164/1a6315b0_9911226.png?width=16
[list]: https://foruda.gitee.com/images/1678607435868247552/890a21c3_9911226.png?width=16
[compound]: https://foruda.gitee.com/images/1678607445511007209/448e8cec_9911226.png?width=16

![Integer][int] 整型 `format_version`: 当前总为 `1`

![List][list] 列表 `size`: 整数列表，用于表示结构大小
-   ![Integer][int] 整型: 结构X轴长
-   ![Integer][int] 整型: 结构Y轴长
-   ![Integer][int] 整型: 结构Z轴长

![Compound][compound] 复合 `structure`: 实际存储结构的数据组

- ![List][list] 列表 `block_indices`: 结构中存储的方块索引。包含两个列表，第一个为实际方块数据，第二个列表对应第一个列表中的方块之内含层(second layer)的方块数据。每一个方块都以一个整型数据，即在方块池(palette)（详见下文）中的索引下标(index)，的形式存储。方块的存储是一维列表，将结构中每个方块依照从 Z 轴到 Y 轴到 X 轴且沿轴正方向的顺序一字排开形成列表。例如，若结构大小为 `[2,3,4]`，则每一层（即包括内含层也是一样的顺序）的24个方块（这个数量是由结构大小决定的，即结构尺寸的乘积）分别对应着如下相对坐标位置的方块：`[(0,0,0), (0,0,1), (0,0,2), (0,0,3), (0,1,0), (0,1,1), (0,1,2), (0,1,3), (0,2,0), (0,2,1), (0,2,2), (0,2,3), (1,0,0), (1,0,1), (1,0,2), (1,0,3), (1,1,0), (1,1,1), (1,1,2), (1,1,3), (1,2,0), (1,2,1), (1,2,2), (1,2,3)]`。若索引下标为 `-1` 则表示此处无方块（即对应“结构空位”），则此处在结构加载时就会保留其原有方块。在我们用结构方块保存结构时这种现象会发生，同时方块的内含层中也大多是无方块的。同时，两个层的方块共享一个方块池

- - ![List][list] of ![Integer][int] 整型列表: 首层(primary layer)方块列表
- - ![List][list] of ![Integer][int] 整型列表: 内含层方块列表。此层通常为空，但若您存储的是《白蛇传》中的水漫金山场景就另当别论了

- ![List][list] of ![Compound][compound] 复合列表 `entities`: 以 NBT 存储的实体列表，其存储格式与在地图文件中存储实体的形式一致。类似 `Pos` 与 `UniqueID` 这样的独立于不同世界中的标签亦会被保存下来，但是《我的世界》加载这样的标签时会将它们覆写为实际值

- ![Compound][compound] 复合 `palette`: 理论上可以包含多种不同名字的方块池(palette)，似乎这样设计是可能要支持以后的对于同一种结构的变体形态。但可惜的是，目前游戏内仅保存和加载名称为 `default` 的方块池

- - ![Compound][compound] 复合 `自定名称` : 单方块池（目前名称别自定，自定了没用，只能是 `default`）

- - - ![List][list] 列表 `block_palette`: 方块及其状态(Block State)之列表，即包含了方块索引中那些索引下标(index)所指代之方块
- - - - ![Compound][compound] 复合: 单方块及其状态
- - - - - ![String][string] 字符串 `name`: 方块ID(identifier)，形如 `minecraft:planks`
- - - - - ![Compound][compound] 复合 `states`: 方块之状态(state)，以键值对的形式出现。例如：`wood_type:"acacia"`、`bite_counter:3`、`open_bit:1b`。其值将转换为 NBT 可接受的类型，如在游戏内枚举出的值(enum values)将转换为字符串(string)、标量(scalar numbers)将被转换为整型(integer)、布尔值(boolean values)会被转为字节型(byte)
- - - - - ![Integer][int] 整型 `version`: 兼容版本(Compatibility versioning number)（当前此文撰写时，对应的版本号是 `17959425`，对应游戏版本 1.19）

- - - ![Compound][compound] 复合 `block_position_data`: 包含结构中各个方块的附加数据(additional data)，每一个键(key)皆为`block_indices` 中的下标索引(index)，表示其对应的方块，数据类型当然为整型(integer)。此处不会保有多层方块的指代，难道你见过草方块里包含着一个指令方块的吗？

- - - - ![Compound][compound] 复合 `方块索引(index)值`: 单方块附加数据(additional block data)以方块之方块索引而对应着此方块

- - - - - ![Compound][compound] 复合 `block_entity_data`: 以 NBT 存储方块实体数据(block entity data)，其存储格式与在地图文件中存储实体的形式一致。同上述实体标签的理，其位置标签(position tag)亦会被保存下来，但是《我的世界》加载这样的标签时会将它们覆写为实际值。不过这时候也不会有其他什么东西跟这玩意手拉手出现了 *\>译注：此处原文为No other objects seem to exist adjacent to this one at this time.应该是说，与`entities`那么多其他的独立于各个世界的标签相比，在方块实体中的算少的了*

![List][list] 列表 `structure_world_origin`: 结构最初保存时的起始点坐标(position)，以三个整型(integer)组成的列表的形式出现。坐标的值即结构方块保存时的坐标加上我们在结构放开里填写的偏移数据。这个坐标用于计算(determine)加载时实体的位置。一个实体的新的绝对坐标由其原始坐标减去结构最初保存时的起始点坐标后，再加上加载起始点的坐标计算而来。

- ![Integer][int] 整型: 结构原 X 坐标
- ![Integer][int] 整型: 结构原 Y 坐标
- ![Integer][int] 整型: 结构原 Z 坐标

以下是一些例子（以Python的数据结构为例）：

```python
# 大小为 1x3x1 (XYZ) 的
# 从下往上分别是一个指令方块、一个铁块和一个空气方块的
# 结构 NBT 数据
{
    'format_version': TAG_Int(1, 'format_version'),
    'size': [TAG_Int(1, None), TAG_Int(3, None), TAG_Int(1, None)],
    'structure': {
        'block_indices': [
            [TAG_Int(0, None), TAG_Int(1, None), TAG_Int(2, None)],
            [TAG_Int(-1, None), TAG_Int(-1, None), TAG_Int(-1, None)]
        ],
        'entities': [],
        'palette': {
            'default': {
                'block_palette': [
                    {
                        'name': TAG_String('minecraft:command_block', 'name'),
                        'states': {
                            'conditional_bit': TAG_Byte(0, 'conditional_bit'),
                            'facing_direction': TAG_Int(1, 'facing_direction')
                        },
                        'version': TAG_Int(17959425, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:iron_block', 'name'),
                        'states': {},
                        'version': TAG_Int(17959425, 'version')
                    },
                    {
                        'name': TAG_String('minecraft:air', 'name'),
                        'states': {},
                        'version': TAG_Int(17959425, 'version')
                    }
                ],
                'block_position_data': {
                    '0': {
                            'Command': TAG_String('help 4', 'Command'),
                            'CustomName': TAG_String('', 'CustomName'),
                            'ExecuteOnFirstTick': TAG_Byte(0, 'ExecuteOnFirstTick'),
                            'LPCommandMode': TAG_Int(0, 'LPCommandMode'),
                            'LPCondionalMode': TAG_Byte(0, 'LPCondionalMode'),
                            'LPRedstoneMode': TAG_Byte(0, 'LPRedstoneMode'),
                            'LastExecution': TAG_Long(0, 'LastExecution'),
                            'LastOutput': TAG_String('', 'LastOutput'),
                            'LastOutputParams': [],
                            'SuccessCount': TAG_Int(0, 'SuccessCount'),
                            'TickDelay': TAG_Int(0, 'TickDelay'),
                            'TrackOutput': TAG_Byte(1, 'TrackOutput'),
                            'Version': TAG_Int(25, 'Version'),
                            'auto': TAG_Byte(0, 'auto'),
                            'conditionMet': TAG_Byte(0, 'conditionMet'),
                            'conditionalMode': TAG_Byte(0, 'conditionalMode'),
                            'id': TAG_String('CommandBlock', 'id'),
                            'isMovable': TAG_Byte(1, 'isMovable'),
                            'powered': TAG_Byte(0, 'powered'),
                            'x': TAG_Int(1, 'x'),
                            'y': TAG_Int(1, 'y'),
                            'z': TAG_Int(1, 'z')
                        }
                }
            }
        }
    },
    'structure_world_origin': [TAG_Int(0, None), TAG_Int(0, None), TAG_Int(0, None)],
}
```

```python
# 大小为 2x2x2 (XYZ) 的
# 全是白色羊毛的
# 结构 NBT 数据
{
    'format_version': TAG_Int(1, 'format_version'),
    'size': [TAG_Int(2, None), TAG_Int(2, None), TAG_Int(2, None)],
    'structure': {
        'block_indices': [
            [
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None),
                TAG_Int(0, None)
            ],
            [
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None),
                TAG_Int(-1, None)
            ]
        ],
        'entities': [],
        'palette': {
            'default': {
                'block_palette': [
                    {
                        'name': TAG_String('minecraft:wool', 'name'),
                        'states': {'color': TAG_String('white', 'color')},
                        'version': TAG_Int(17959425, 'version')
                    }
                ],
                'block_position_data': {}
            }
        }
    },
    'structure_world_origin': [TAG_Int(0, None), TAG_Int(0, None), TAG_Int(0, None)]
}
```

源代码可参照此处，作者金羿。