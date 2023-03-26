# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TrimMCStruct",
    version="0.0.1",
    author="Eilles Wan, bgArray, phoenixr-codes(original author) ",
    author_email="TriM-Organization@hotmail.com",
    description="读写操作《我的世界》.MCSTRUCTURE文件\n"
    " Read and write Minecraft .mcstructure files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TriM-Organization/TrimMCStruct",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # 需要安装的依赖
    install_requires=[
        "numpy>=1.21",
        "pynbt>=2",
    ],
)
