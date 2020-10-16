CREATE TABLE recipes_to_categories (
    recipe_id TEXT,
    category_id INTEGER,
    FOREIGN KEY(recipe_id) REFERENCES recipes(uid)
    FOREIGN KEY(category_id) REFERENCES categories(id)
);
