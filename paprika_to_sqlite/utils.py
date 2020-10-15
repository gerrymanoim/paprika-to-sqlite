import sqlite3

RECIPE_SCHEMA = {
    "directions": "TEXT",
    "difficulty": "TEXT",
    "ingredients": "TEXT",
    "description": "TEXT",
    "photodata": "BLOB",  # TODO check
    "source": "TEXT",
    "name": "TEXT",
    "notes": "TEXT",
    "total_time": "TEXT",
    "hash": "TEXT",
    "categories": [],  # TODO build a categories table
    "photo": "TEXT",
    "created": "TEXT",  # ISO8601
    "source_url": "http:\/\/smittenkitchen.com\/blog\/2015\/07\/very-blueberry-scones\/",
    "servings": "TEXT",
    "prep_time": "TEXT",
    "photo_hash": "TEXT",
    "rating": "INTEGER",
    "image_url": "TEXT",
    "nutritional_info": "TEXT",
    "uid": "TEXT",
    "cook_time": "TEXT",
    "photos": [],  # TODO
    "photo_large": "TEXT",
}


def create_table_sql() -> str:
    pass


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


def generate_and_populate_fts(conn, created_tables, cols, foreign_keys):
    """
    Partially via
    via https://github.com/simonw/csvs-to-sqlite/blob/master/csvs_to_sqlite/utils.py
    """
    fts_version = best_fts_version()
    sql = []
    fts_cols = ", ".join('"{}"'.format(c) for c in cols)
    for table in created_tables:
        sql.append(
            'CREATE VIRTUAL TABLE "{content_table}_fts" USING {fts_version} ({cols}, content="{content_table}")'.format(
                cols=fts_cols, content_table=table, fts_version=fts_version
            )
        )
        if not foreign_keys:
            # Select is simple:
            select = "SELECT rowid, {cols} FROM [{content_table}]".format(
                cols=fts_cols, content_table=table
            )
        else:
            # Select is complicated:
            # select
            #     county, precinct, office.value, district.value,
            #     party.value, candidate.value, votes
            # from content_table
            #     left join office on content_table.office = office.id
            #     left join district on content_table.district = district.id
            #     left join party on content_table.party = party.id
            #     left join candidate on content_table.candidate = candidate.id
            # order by content_table.rowid
            select_cols = []
            joins = []
            table_seen_count = {}
            for col in cols:
                if col in foreign_keys:
                    other_table, label_column = foreign_keys[col]
                    seen_count = table_seen_count.get(other_table, 0) + 1
                    table_seen_count[other_table] = seen_count
                    alias = ""
                    if seen_count > 1:
                        alias = "table_alias_{}_{}".format(
                            hashlib.md5(
                                other_table.encode("utf8")
                            ).hexdigest(),
                            seen_count,
                        )
                    select_cols.append(
                        '[{}]."{}"'.format(alias or other_table, label_column)
                    )
                    joins.append(
                        'left join [{other_table}] {alias} on [{table}]."{column}" = [{alias_or_other_table}].id'.format(
                            other_table=other_table,
                            alias_or_other_table=alias or other_table,
                            alias=alias,
                            table=table,
                            column=col,
                        )
                    )
                else:
                    select_cols.append('"{}"'.format(col))
            select = "SELECT [{content_table}].rowid, {select_cols} FROM [{content_table}] {joins}".format(
                select_cols=", ".join("{}".format(c) for c in select_cols),
                content_table=table,
                joins="\n".join(joins),
            )
        sql.append(
            'INSERT INTO "{content_table}_fts" (rowid, {cols}) {select}'.format(
                cols=fts_cols, content_table=table, select=select
            )
        )
    conn.executescript(";\n".join(sql))
