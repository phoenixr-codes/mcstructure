<p align="center">
	<img
		src="https://raw.githubusercontent.com/phoenixr-codes/mcstructure/main/logo.png"
		width="120px"
		align="center" alt="mcstructure logo"
	/>
	<h1 align="center">mcstructure</h1>
	<p align="center">
		《我的世界》<code>.mcstructure</code> 文件的读写操作库
	</p>
</p>


🌍 此介绍文件亦可见于以下语种：

* [🇬🇧 英文](./README.md)
* [🇩🇪 德文](./README_DE.md) *(未及时更新)*

<!-- Not really accessible ♿️ but we get a prettier line
than the default "<hr/>" or "---" --> 
<h2></h2>

[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/mcstructure/badge/?style=for-the-badge&version=latest)](https://mcstructure.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/mcstructure?style=for-the-badge)](https://pypi.org/project/mcstructure)

_在整个项目中（且更官方地是在“大一统更新”("Better Together Update")之后，名词《我的世界》("Minecraft")所指代的均为基岩版("Bedrock Edition")。_

_此库中的所有特性也是仅仅针对基岩版的。_

> [!WARNING]
> **请注意**
> 此项目目前仍属于 **BETA** 版本，因此部分特性可能并未启用或在未经示警的情况下频繁更改。

<!-- start elevator-pitch -->

此库可以让您以代码实现对 *《我的世界》* 结构文件的创建与编辑。
您能够凭此而将您自己的结构存储为 `.mcstructure` 文件，因而可以使之用于行为包中，或者发展出更厉害的用途。

当然，通过此库您也可以通过此库来读取(read)这些在游戏中通过*结构方块*保存的结构文件，从而获取(identify)其中存储之方块与实体之类。

<!-- end elevator-pitch -->

下载安装
------------

```console
pip install mcstructure
```


基本用法
-----------

1.	写入结构文件

	```python
	# 导入库
	from mcstructure import Block, Structure

	# 实例化对象 Structure
	struct = Structure(
		(7, 7, 7),  # 声明结构大小
		Block("minecraft:wool", color = "red")	# 预填充方块
	)

	# 设定方块
	(struct
		.set_block((1, 1, 1), Block("minecraft:grass"))
		.set_block((2, 2, 2), Block("minecraft:grass"))
		.set_block((3, 3, 3), Block("minecraft:grass"))
		.set_block((4, 4, 4), Block("minecraft:grass"))
		.set_block((5, 5, 5), Block("minecraft:grass"))
		.set_block((6, 6, 6), Block("minecraft:grass"))
	)

	# 写入文件
	with open("house.mcstructure", "wb") as f:
		struct.dump(f)

	```

2.	读取结构文件

	```python
	with open("house.mcstructure", "rb") as f:
		struct = Structure.load(f)

	```

妙用链接
------------

* 📖 [此项目之文档](https://mcstructure.readthedocs.io/en/latest/)
* 📁 [此项目之源码](https://github.com/phoenixr-codes/mcstructure)
* 🐍 [PyPI](https://pypi.org/project/mcstructure/)

### 其他资源

* 👋 [结构方块的简介](https://learn.microsoft.com/en-us/minecraft/creator/documents/introductiontostructureblocks)
* 📖 [基岩版维基](https://wiki.bedrock.dev/nbt/mcstructure.html#file-format)
_译注：文件结构文档已经被我翻译了，详见[我的译本](https://gitee.com/TriM-Organization/mcstructure/blob/main/docs/mcstructure%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84.md)_
--------------------------------------------

NOT AN OFFICIAL MINECRAFT PRODUCT.
NOT APPROVED BY OR ASSOCIATED WITH MOJANG.

此项目并非一个官方 《我的世界》（*Minecraft*）项目

此项目不隶属或关联于 Mojang Studios
