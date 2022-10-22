from tkinter.messagebox import NO
from flask import Flask, render_template, request, flash, redirect,session
from werkzeug.security import check_password_hash

import os
import random
from project.db import Db
from project.account import (
    add_new_account,
    search_account_by_id,
    convert_account_obj, search_account_by_email
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
from project.comment import add_comment

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

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if 'username' in session:
                # Will need to be changed to redirect to a user's page
                return redirect('/')

            email = request.form['email']
            user = search_account_by_email(email)

            if user:
                if check_password_hash(user[3], request.form['password']):
                    session['username'] = user[1]
                    redirect_url = request.args.get('redirect_url')
                    if redirect_url:
                        return redirect(redirect_url)
                    else:
                        # Need to specify default URL after login
                        return redirect('/')
                else:
                    flash("Wrong password")
                    return render_template("/login.html")
            else:
                flash("That account does not exist")
                return render_template("/login.html")

        return render_template("/login.html")

    @app.route("/logout", methods=["GET"])
    def logout():
        if 'username' in session:
            session.pop('username', None)
            return redirect('/')
        return "user not logged in", 401

    # For testing purposes
    @app.route("/user", methods=["GET"])
    def get_current_user():
        if 'username' in session:
            # Add logic to read info from session token
            return "Someone is in", 200
        return "No user", 401


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

    @app.route("/api/comments/add", methods=["POST"])
    def api_add_comment_to_recipe():

        try:
            comment_title = request.args.get("title", type=str)
            comment_body = request.args.get("body", type=str)
            author_id = request.args.get("author_id", type=int)
            recipe_id = request.args.get("recipe_id", type=int)

            assert comment_title is not None
            assert comment_body is not None
        except:
            return "Invalid request parameters", 400

        if search_account_by_id(author_id) is None:
            return "Invalid author id", 404

        if search_recipe_by_id(recipe_id) is None:
            return "Invalid recipe id", 404

        return add_comment(comment_title, comment_body, author_id, recipe_id)


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

