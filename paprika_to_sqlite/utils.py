import itertools
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

SCHEMA_DIR = Path(__file__).parent / "sql"


def best_fts_version():
    """"
    Discovers the most advanced supported SQLite FTS version
    via https://github.com/simonw/csvs-to-sqlite/blob/master/csvs_to_sqlite/utils.py
    """
    conn = sqlite3.connect(":memory:")
    for fts in ("FTS5", "FTS4", "FTS3"):
        try:
            conn.execute("CREATE VIRTUAL TABLE v USING {} (t);".format(fts))
            return fts
        except sqlite3.OperationalError:
            continue
    return None


def create_table(conn: sqlite3.Connection, table_name: str):
    schema_file = SCHEMA_DIR / f"{table_name}.sql"
    if not schema_file.exists():
        known_schemas = [fl.name for fl in SCHEMA_DIR.iterdir()]
        raise ValueError(
            f"""
            Being asked to create unknown table {table_name}.
            I only know about {known_schemas}
            """
        )
    creation_statement = schema_file.read_text()
    cur = conn.cursor()
    cur.execute(creation_statement)
    conn.commit()


def build_insertion_statement(table_name: str, d: Dict[str, Any]):
    cols = ", ".join(d.keys())
    placeholders = ":" + ", :".join(d.keys())
    return f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders});"


def build_recipe_table(
    conn: sqlite3.Connection, recipe_list: List[Dict[str, Any]]
):
    """Build the table containing recipe data

    Parameters
    ----------
    conn : sqlite3.Connection
        Connnection to the db
    recipe_list : List[Dict[str, Any]]
        A non-empty list of recipe dicts
    """
    create_table(conn, "recipes")

    insertion_statement = build_insertion_statement("recipes", recipe_list[0])
    cur = conn.cursor()
    cur.executemany(insertion_statement, recipe_list)
    conn.commit()


def build_list_table_with_mapping(
    conn: sqlite3.Connection,
    table_name: str,
    single_item_name: str,
    recipe_to_list: Dict[str, List[str]],
):
    mapping_table_name = f"recipes_to_{table_name}"
    create_table(conn, table_name)
    create_table(conn, mapping_table_name)
    if len(recipe_to_list) > 0:
        cur = conn.cursor()
        unique_items = set(
            itertools.chain.from_iterable(recipe_to_list.values())
        )
        item_ids = list(enumerate(unique_items))
        cur.executemany(
            f"INSERT INTO {table_name} (id, {single_item_name}) values (?,?);",
            item_ids,
        )
        item_to_id = {item: _id for _id, item in item_ids}
        mapping_table_values = (
            (recipe_id, item_to_id[category])
            for recipe_id, recipe_categories in recipe_to_list.items()
            for category in recipe_categories
        )
        insert_statement = f"""
            INSERT INTO
                {mapping_table_name} (recipe_id, {single_item_name}_id)
            VALUES
                (?, ?)
            ;
        """
        cur.executemany(
            insert_statement, mapping_table_values,
        )
        conn.commit()


def build_fts_table(conn: sqlite3.Connection):
    """
    TOOD: Is there a better way to do this?
    """
    fts_version = best_fts_version()
    fts_cols = ", ".join(
        ["directions", "ingredients", "source", "name", "notes"]
    )
    content_table = "recipes"
    build_fts_statement = f"""
        CREATE VIRTUAL TABLE {content_table}_fts USING {fts_version} (
            {fts_cols},
            content="{content_table}"
        );
        INSERT INTO "{content_table}_fts"
            (rowid, {fts_cols})
        SELECT
            rowid, {fts_cols}
        FROM [{content_table}]
        ;
    """
    cur = conn.cursor()
    cur.executescript(build_fts_statement)
    conn.commit()
