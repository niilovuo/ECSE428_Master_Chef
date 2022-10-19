from flask import Flask, render_template, request, flash
import os
import random

from project.comment import search_comment_by_id, delete_comment_by_id
from project.db import Db
from project.account import (
    add_new_account,
    search_account_by_id,
    convert_account_obj
)
from project.tag_query import (
    get_all_tags,
    get_tags_of_recipe
)
from project.ingredient_query import get_ingredients_of_recipe
from project.recipe_query import (
    search_recipes_by_filter,
    search_recipe_by_id,
    convert_recipe_obj
)

def create_app():
    app = Flask(__name__)
    app.secret_key = b'_123kjhmnb23!!'

    @app.route("/")
    def home():
        return render_template("/home.html", value = random.randrange(1024))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form['username']
            email = request.form['email']
            password = request.form['password']

            err = add_new_account(name, email, password)
            if err is not None:
                flash(err)
                return render_template("/register.html")

            # return to register page with "Success" for now
            flash("Success")
            return render_template("/register.html")

        return render_template("/register.html")

    @app.route("/search")
    def search():
        return render_template("/search_recipes.html")

    @app.route("/recipes/<int:id>")
    def lookup_recipe(id):
        recipe = search_recipe_by_id(id)
        if recipe is None:
            return render_template("/recipe.html",
                                   recipe=None, author=None, tags=[], ingredients=[])

        recipe = convert_recipe_obj(recipe)
        author = convert_account_obj(search_account_by_id(recipe["author"]))
        tags = get_tags_of_recipe(id)
        ingredients = get_ingredients_of_recipe(id)
        return render_template("/recipe.html",
                               recipe=recipe, author=author, tags=tags, ingredients=ingredients)

    @app.route("/api/search")
    def api_search():
        try:
            title = request.args.get("q", type=str)
            start = request.args.get("start", 0, type=int)
            tags = request.args.getlist("tags[]", type=str)

            assert title is not None
        except:
            return "Invalid request parameters", 400

        (recipes, err) = search_recipes_by_filter(title, tags, start)
        if recipes is None:
            return err, 400

        # we need to explicitly convert the time fields to strings
        return [convert_recipe_obj(recipe) for recipe in recipes]

    @app.route("/api/tags")
    def api_list_tags():
        return get_all_tags()

    @app.route("/api/users/<int:id>")
    def api_lookup_account(id):
        account = search_account_by_id(id)
        if account is None:
            return "Invalid account id", 404

        return convert_account_obj(account)

    @app.route("/api/recipes/<int:id>")
    def api_lookup_recipe(id):
        recipe = search_recipe_by_id(id)
        if recipe is None:
            return "Invalid recipe id", 404

        return convert_recipe_obj(recipe)

    @app.route("/api/recipes/<int:id>/tags")
    def api_lookup_recipe_tags(id):
        if search_recipe_by_id(id) is None:
            return "Invalid recipe id", 404

        tags = get_tags_of_recipe(id)
        return tags

    @app.route("/api/recipes/<int:id>/ingredients")
    def api_lookup_recipe_ingredients(id):
        if search_recipe_by_id(id) is None:
            return "Invalid recipe id", 404

        ingredients = get_ingredients_of_recipe(id)
        return ingredients


    @app.route("/api/comment/<int:id>", methods=["DELETE"])
    def delete_comment(id):
        comment = search_comment_by_id(id)
        user_id = int(request.form['user_id'])
        user_login = request.form['user_id']
        if comment is None:
            return "This comment does not exist", 404
        author_id = comment[3]
        recipe_id = comment[4]
        auth_id_list = [author_id]
        recipe = search_recipe_by_id(recipe_id)
        if recipe:
            auth_id_list.append(recipe[5])
        if user_id not in auth_id_list:
            return "no permission to delete comment", 400
        flag, err = delete_comment_by_id(id, user_login)
        if flag:
            return 'delete comment success', 200
        else:
            return "This comment does not exist", 404

    return app

if __name__ == "__main__":
    pg_user = os.getenv("POSTGRES_USER", "postgres")
    db_args = {
        "password": os.getenv("POSTGRES_PASSWORD"),
        "user": pg_user,
        "dbname": os.getenv("POSTGRES_DB", pg_user),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", 5432)
    }

    Db.init_session(**db_args)
    Db.setup_tables()

    app = create_app()
    app.debug = os.getenv("DEBUG") == "true"
    app.run()
    Db.deinit_session()

