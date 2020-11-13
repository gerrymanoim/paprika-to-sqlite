from datasette import hookimpl
from datasette.utils.asgi import Response


def can_render_paprika_recipe(database, table, view_name):
    return table == "recipes" and view_name == "row"


async def paprika_recipe_link(request, datasette, rows):
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
        "render": paprika_recipe_link,
        "can_render": can_render_paprika_recipe,  # Optional
    }


async def paprika_recipe_route(request, datasette):
    r = await datasette.client.get(
        f'paprika/recipes/{request.url_vars["recipe_id"]}.json'
    )
    row_data = r.json()

    return Response.html(
        await datasette.render_template(
            "recipe.html",
            dict(zip(row_data["columns"], row_data["rows"][0])),
            request=request,
        )
    )


@hookimpl
def register_routes():
    return [(r"^/-/paprika-recipe/(?P<recipe_id>.*)$", paprika_recipe_route)]
