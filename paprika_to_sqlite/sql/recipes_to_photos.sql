CREATE TABLE recipes_to_photos (
    recipe_id TEXT,
    photo_id INTEGER,
    FOREIGN KEY(recipe_id) REFERENCES recipes(uid)
    FOREIGN KEY(photo_id) REFERENCES photos(id)
);
