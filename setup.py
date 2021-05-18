from os import path

import setuptools

install_requires = ["bip-utils", "shamir-mnemonic", "click"]

test_requires = ["pytest", "pytest-cov", "pytest-mock"]


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="seedsplit",
    version="0.1.0",
    author="Paul Angerer",
    author_email="etimoz@users.noreply.github.com",
    description="Tool for splitting a seed into multiple shards.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/etimoz/seedsplit/",
    keywords="bip39 bip-39 seed split shards cli parts cryptocurrency wallet",
    zip_safe=False,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={"test": test_requires + install_requires},
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={"console_scripts": ["seedsplit = seedsplit.__main__:cli"]},
)
