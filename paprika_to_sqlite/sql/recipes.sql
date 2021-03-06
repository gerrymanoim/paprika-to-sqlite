CREATE TABLE recipes(
    uid TEXT NOT NULL PRIMARY KEY,
    cook_time TEXT,
    created TEXT,
    description TEXT,
    difficulty TEXT,
    directions TEXT,
    hash TEXT,
    image_url TEXT,
    ingredients TEXT,
    name TEXT,
    notes TEXT,
    nutritional_info TEXT,
    photo TEXT,
    photo_data BLOB,
    photo_hash TEXT,
    photo_large TEXT,
    prep_time TEXT,
    rating INTEGER,
    servings TEXT,
    source TEXT,
    source_url TEXT,
    total_time TEXT
)
;
