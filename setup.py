from setuptools import setup, find_packages
import io
import os

VERSION = "0.2.1"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="paprika_to_sqlite",
    description="Convert Paprika Recipes files into a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Gerry Manoim",
    author_email="Gerry Manoim <gerrymanoim@gmail.com>",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    extras_require={"datasette": ["datasette"], "dev": ["flake8", "black"], },
    entry_points={
        "datasette": ["paprika = paprika_to_sqlite.datasette_paprika"],
        "console_scripts": ["paprika-to-sqlite = paprika_to_sqlite.cli:cli", ],
    },
    url="https://github.com/gerrymanoim/paprika-to-sqlite",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ],
)
