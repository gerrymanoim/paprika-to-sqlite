from datasette import hookimpl
from datasette.utils.asgi import Response


def can_render_paprika_recipe(database, table, view_name):
    return database == "paprika" and table == "recipes" and view_name == "row"


async def paprika_recipe(request, datasette, rows):
    row = rows[0]

    return Response.html(
        await datasette.render_template(
            "recipe.html", dict(zip(row.keys(), tuple(row))), request=request,
        )
    )


@hookimpl
def register_output_renderer(datasette):
    return {
        "extension": "paprikarecipe",
        "render": paprika_recipe,
        "can_render": can_render_paprika_recipe,  # Optional
    }


@hookimpl
def register_routes():
    return [
        (r"^/paprika-recipe/(?P<recipe_id>.*)$", paprika_recipe)
    ]
