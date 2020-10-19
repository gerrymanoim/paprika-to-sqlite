# Paprika To SQLite

[![PyPI version](https://badge.fury.io/py/paprika-to-sqlite.svg)](https://badge.fury.io/py/paprika-to-sqlite)

Takes a `paprikarecipe` file exported from [Paprika](https://www.paprikaapp.com/) and converts it to an sqlite db.

Tables:

- `recipes`
- `recipes_to_categories`
- `recipes_to_photos`
- `categories`
- `photos`


Useful with [Datasette](https://datasette.io/).

## Install

```
pip install paprika-to-sqlite
```

## Usage

```
paprika-to-sqlite --version
paprika-to-sqlite --help
paprika-to-sqlite my_export.paprikarecipes paprika.db
```
