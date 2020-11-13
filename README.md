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
# or pip install paprika-to-sqlite[datasette]
```

## Usage

```
paprika-to-sqlite --version
paprika-to-sqlite --help
paprika-to-sqlite my_export.paprikarecipes paprika.db
```

### Usage with datasette

If you have `paprika-to-sqlite` and `datasette` installed in the same environment, you can use `datasette` to look at any recipe. First, launch datasette:

```
datasette paprika.db
```

This will add a `paprikarecipe` link to individual row pages:

![Link Image](https://github.com/gerrymanoim/paprika-to-sqlite/raw/master/img/link.png)

and a url handler for `/-/paprika-recipe/<recipe-id>`. This will display the recipe as a simple webpage:

![Page Image](https://github.com/gerrymanoim/paprika-to-sqlite/raw/master/img/page.png)
