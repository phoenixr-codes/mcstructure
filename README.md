<p align="center">
	<img
		src="https://gitee.com/TriM-Organization/mcstructure/raw/resources/logo.png"
		width="120px"
		align="center" alt="mcstructure logo"
	/>
	<h1 align="center">mcstructure</h1>
	<p align="center">
		对于《我的世界》<code>.mcstructure</code> 文件的读写操作库
	</p>
</p>


[![][GitHub: phoenixR]](https://github.com/phoenixr-codes)
[![][Gitee: Eilles]](https://gitee.com/EillesWan)
[![][GitHub: Eilles]](https://gitHub.com/EillesWan)
[![][Bilibili: Eilles]](https://space.bilibili.com/397369002/)


[![CodeStyle: black]](https://github.com/psf/black)
[![][python]](https://www.python.org/)
[![][license]](LICENSE)
[![][release]](../../releases)


[![GiteeStar](https://gitee.com/TriM-Organization/mcstructure/badge/star.svg?theme=gray)](https://gitee.com/TriM-Organization/mcstructure/stargazers)
[![GiteeFork](https://gitee.com/TriM-Organization/mcstructure/badge/fork.svg?theme=gray)](https://gitee.com/TriM-Organization/mcstructure/members)
[![GitHub Repo stars](https://img.shields.io/github/stars/TriM-Organization/TrimMCStruct?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/TrimMCStruct/stargazers)
[![GitHub Repo Forks](https://img.shields.io/github/forks/TriM-Organization/TrimMCStruct?color=white&logo=GitHub&style=plastic)](https://github.com/TriM-Organization/TrimMCStruct/forks)

*在此项目中（且更官方地是在“大一统更新”("Better Together Update")之后）专有名词《我的世界》("Minecraft")所指代的均为基岩版("Bedrock Edition")。*

_此项目中的所有特性也是仅仅针对基岩版的。_

> **请注意**
> 此项目目前仍属于 BETA 版本，因此很多的特性可能无法实现。

此库可以让您以代码实现对 *《我的世界》* 结构文件的创建(create)与编辑(edit)。
您能够凭此而将您自己的结构存储为 `.mcstructure` 文件，因而可以使之用于行为包中，或者发展出更优秀的用途。

当然，通过此库您也可以通过此库来读取(read)这些结构文件。
以获取(identify)其中存储之方块与实体之类。

*译注：虽然上面看似废话，但实际上也是一个介绍好吧……QwQ*

下载安装
------------

```bash
pip install mcstructure
```


基础用法
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
		.set_block((1, 1, 1), Block("minecraft","grass"))
		.set_block((2, 2, 2), Block("minecraft","grass"))
		.set_block((3, 3, 3), Block("minecraft","grass"))
		.set_block((4, 4, 4), Block("minecraft","grass"))
		.set_block((5, 5, 5), Block("minecraft","grass"))
		.set_block((6, 6, 6), Block("minecraft","grass"))
	)

	# 写入文件
	with open("something.mcstructure", "wb") as f:
		struct.dump(f)

	```

2.	读取结构文件

	```python
	with open("something.mcstructure", "rb") as f:
		struct = Structure.load(f)

	```

--------------------------------------------

NOT AN OFFICIAL MINECRAFT PRODUCT.
NOT APPROVED BY OR ASSOCIATED WITH MOJANG.

此项目并非一个官方 《我的世界》（*Minecraft*）项目

此项目不隶属或关联于 Mojang Studios



[GitHub: phoenixR]: https://img.shields.io/badge/GitHub-phoenixR-00A1E7?style=plastic

[Bilibili: Eilles]: https://img.shields.io/badge/Bilibili-%E5%87%8C%E4%BA%91%E9%87%91%E7%BE%BF-00A1E7?style=plastic
[Gitee: Eilles]: https://img.shields.io/badge/Gitee-EillesWan-00A1E7?style=plastic
[GitHub: Eilles]: https://img.shields.io/badge/GitHub-EillesWan-00A1E7?style=plastic

[CodeStyle: black]: https://img.shields.io/badge/code%20style-black-121110.svg?style=plastic
[python]: https://img.shields.io/badge/python-3.8-AB70FF?style=plastic
[release]: https://img.shields.io/github/v/release/EillesWan/Musicreater?style=plastic
[license]: https://img.shields.io/badge/Licence-Apache-228B22?style=plastic