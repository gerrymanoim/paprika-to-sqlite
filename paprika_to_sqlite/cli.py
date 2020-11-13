import gzip
import json
import sqlite3
from pathlib import Path
from zipfile import ZipFile

import click

from .utils import (
    build_fts_table,
    build_list_table_with_mapping,
    build_recipe_table,
)


@click.command()
@click.argument("export_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("dbname", nargs=1)
@click.version_option()
def cli(
    export_file, dbname, table="recipes",
):
    conn = sqlite3.connect(dbname)
    # TODO unecessary
    export_file = Path(export_file)
    if export_file.suffix != ".paprikarecipes":
        # TODO - report this better?
        raise ValueError(f"Unknown filetype {export_file.suffix}")

    click.echo(f"Reading {export_file}")

    zip_file = ZipFile(export_file)

    recipe_list = []
    recipes_to_categories = dict()
    recipes_to_photos = dict()

    # A "paprikarecipe" file is a zip file containing gzipped JSON files
    for fl in zip_file.namelist():
        with zip_file.open(fl) as recipe_file:
            with gzip.open(recipe_file) as recipe_json:
                recipe = json.load(recipe_json)
                if recipe["photo_data"] is not None:
                    recipe["photo_data"] = recipe["photo_data"].encode()
                recipes_to_categories[recipe["uid"]] = recipe.pop("categories")
                recipes_to_photos[recipe["uid"]] = [
                    photo_data.encode() for photo_data in recipe.pop("photos")
                ]
                recipe_list.append(recipe)

    click.echo(f"Got {len(recipe_list)} recipes")
    if len(recipe_list) == 0:
        click.echo("Nothing to do. Exiting. ", err=True)
    else:
        click.echo("Building the recipe table. ")
        build_recipe_table(conn, recipe_list)
        click.echo("Building the categories tables. ")
        build_list_table_with_mapping(
            conn, "categories", "category", recipes_to_categories,
        )
        click.echo("Building the photos tables. ")
        build_list_table_with_mapping(
            conn, "photos", "photo", recipes_to_photos,
        )
        click.echo("Building the recipes FTS tables. ")
        build_fts_table(conn)
        click.echo("All done!")

    conn.close()
