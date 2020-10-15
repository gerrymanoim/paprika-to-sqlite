import gzip
import json
import os
import sqlite3

from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import click


@click.command()
@click.argument("export_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("dbname", nargs=1)
@click.version_option()
def cli(
    export_file,
    dbname,
    table="recipes",
):
    conn = sqlite3.connect(dbname)
    # TODO unecessary
    export_file = Path(export_file)
    if export_file.suffix != ".paprikarecipes":
        raise ValueError(f"Unknown filetype {export_file.suffix}")

    zip_file = ZipFile(export_file)

    recipe_list = []

    for fl in zip_file.namelist():
        with zip_file.open(fl) as recipe_file:
            with gzip.open(recipe_file) as recipe_json:
                recipe_list.append(json.load(recipe_json))
