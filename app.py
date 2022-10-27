from flask import Flask, render_template, request, flash, redirect,session
from werkzeug.security import check_password_hash

import os
import random
from project.db import Db
from project.account import (
    add_new_account,
    search_account_by_id,
    delete_account_by_id,
    search_account_by_name,
    search_account_by_email,
    convert_account_obj
)
from project.recipe import (add_tag_to_recipe, create_recipe, edit_recipe, remove_tag_of_recipe)
from project.tag_query import (
    get_all_tags,
    get_tags_of_recipe
)
from project.ingredient_query import get_ingredients_of_recipe
from project.recipe_query import (
    search_recipes_by_filter,
    search_recipe_by_id,
    search_recipes_by_author,
    convert_recipe_obj
)
from project.comment import add_comment, search_comment_by_id, delete_comment_by_id


def create_app(setup_db=True):
    app = Flask(__name__)
    app.secret_key = b'_123kjhmnb23!!'

    pg_user = os.getenv("POSTGRES_USER", "postgres")
    db_args = {
        "password": os.getenv("POSTGRES_PASSWORD"),
        "user": pg_user,
        "dbname": os.getenv("POSTGRES_DB", pg_user),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", 5432)
    }

    if setup_db:
        with app.app_context():
            Db.init_session(**db_args)
            Db.setup_tables()
            app.teardown_appcontext(lambda e: Db.deinit_session())

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

    @app.route("/setting")
    def account_setting():
        return render_template("/setting.html")

    @app.route("/delete_account")
    def delete_account():
        if 'id' in session:
            delete_account_by_id(session.get('id'))
            session.pop('id', None)
            return render_template('/account_delete.html')
        else:
            flash('Your account cannot be deleted at the moment')
            return redirect('/setting')

    @app.route("/login", methods=["GET", "POST"])
    def login():
        redirect_url = request.args.get('redirect_url', default='/profile')
        if 'id' in session:
            return redirect(redirect_url)

        if request.method == "POST":
            email = request.form['email']
            user = search_account_by_email(email)

            if user:
                if check_password_hash(user[3], request.form['password']):
                    session['id'] = user[0]
                    return redirect(redirect_url)
                else:
                    flash("Wrong password")
                    return render_template("/login.html", redirect_url=redirect_url)
            else:
                flash("That account does not exist")
                return render_template("/login.html", redirect_url=redirect_url)

        return render_template("/login.html", redirect_url=redirect_url)

    @app.route("/logout", methods=["GET"])
    def logout():
        if 'id' in session:
            session.pop('id', None)
            return redirect('/')
        return "user not logged in", 401

    @app.route("/profile")
    @app.route("/profile/<int:id>")
    def user_profile(id=None):
        uses_login_info = id is None
        if uses_login_info:
            id = session.get("id")
            if not id:
                return redirect("/login")

        current_user = convert_account_obj(search_account_by_id(id))
        recipes = []
        if not current_user:
            if uses_login_info:
                # but the account no longer exists, assume the worst and logout
                return redirect("/logout")
        else:
            recipes = search_recipes_by_author(id)
            recipes = [convert_recipe_obj(e) for e in recipes]

        return render_template("/profile.html", user=current_user, recipes=recipes)

    # For testing purposes
    @app.route("/user", methods=["GET"])
    def get_current_user():
        if 'id' in session:
            # Add logic to read info from session token
            return "Someone is in", 200
        return "No user", 401


    @app.route("/search")
    def search():
        title = request.args.get("q", "")
        return render_template("/search_recipes.html", default_query=title)

    @app.route("/recipes/<int:id>")
    def lookup_recipe(id):
        recipe = search_recipe_by_id(id)
        if recipe is None:
            return render_template("/recipe.html",
                                   recipe=None, author=None, tags=[], ingredients=[],
                                   allow_edits=False)

        recipe = convert_recipe_obj(recipe)
        author = convert_account_obj(search_account_by_id(recipe["author"]))
        tags = get_tags_of_recipe(id)
        ingredients = get_ingredients_of_recipe(id)
        allow_edits = session.get('id') == recipe["author"]
        return render_template("/recipe.html",
                               recipe=recipe, author=author, tags=tags, ingredients=ingredients,
                               allow_edits=allow_edits)
                               
    @app.route("/recipes/create")
    def render_create_recipe():
        if 'id' not in session:
            flash("Not logged in")
            return redirect("/")
        return render_template("/upsert_recipe.html", recipe=None, ingredients=[])

    @app.route("/recipes/edit/<int:id>")
    def render_edit_recipe(id):
        if "id" not in session:
            flash("Not logged in")
            return redirect("/")
        recipe = search_recipe_by_id(id)
        if recipe is None:
            flash("Recipe does not exist")
            return redirect("/")
        recipe = convert_recipe_obj(recipe)
        author = convert_account_obj(search_account_by_id(recipe["author"]))
        if author is None or author["id"] != session["id"]:
            flash("Cannot edit this recipe")
            return redirect("/")
        ingredients = [{"name": e[1], "quantity": e[2]} for e in get_ingredients_of_recipe(id)]
        return render_template("/upsert_recipe.html", recipe=recipe, ingredients=ingredients)

    @app.route("/recipes/<int:id>/tags", methods=["POST"])
    def add_tag(id):
        if 'id' not in session:
            return redirect(f"/login?redirect_url=/recipes/{id}")

        user_id = session['id']
        tag = request.form['tag']
        err = add_tag_to_recipe(tag, id, user_id)

        if err:
            flash(err)

        # whatever happens, just redirect to the recipe page
        return redirect(f"/recipes/{id}")

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

    @app.route("/api/recipes/add", methods=["POST"])
    def api_create_recipe():
        data = request.form.to_dict()
        try:
            result = create_recipe(data, session["id"])
            return redirect("/recipes/{}".format(result))
        except Exception as e:
            flash("Could not create recipe")
            return redirect("/")
        
    @app.route("/api/recipes/edit/<int:id>", methods=["POST"])
    def api_edit_recipe(id):
        data = request.form.to_dict()
        try:
            result = edit_recipe(id, data, session["id"])
            return redirect("/recipes/{}".format(result))
        except Exception as e:
            flash("Could not update recipe")
            return redirect("/")
        
        
    
    @app.route("/api/recipes/<int:id>/ingredients")
    def api_lookup_recipe_ingredients(id):
        if search_recipe_by_id(id) is None:
            return "Invalid recipe id", 404

        ingredients = get_ingredients_of_recipe(id)
        return ingredients

    @app.route("/api/comments/add", methods=["POST"])
    def api_add_comment_to_recipe():

        data = request.get_json()

        try:
            comment_title = data.get('comment_title')
            comment_body = data.get('comment_body')
            recipe_id = int(data.get('recipe_id'))
            author_id = session['id']

            assert comment_title is not None
            assert comment_body is not None
        except:
            return "Invalid request parameters", 400

        if search_account_by_id(author_id) is None:
            return "Invalid author id", 404

        if search_recipe_by_id(recipe_id) is None:
            return "Invalid recipe id", 404

        new_id = add_comment(comment_title, comment_body, author_id, recipe_id)
        return (str(new_id), 200) if isinstance(new_id, int) else (str(new_id), 500)


    @app.route("/api/comments/<int:id>", methods=["DELETE"])
    def delete_comment(id):
        comment = search_comment_by_id(id)
        user_id = session.get('id')
        if not user_id:
            return "No user", 404
        if comment is None:
            return "This comment does not exist", 404
        author_id = comment[3]
        err = delete_comment_by_id(id, user_id, author_id)
        if not err:
            return 'delete comment success', 200
        else:
            return err, 404

    @app.route("/api/recipes/<int:recipe_id>/tags/<tag_name>", methods=["DELETE"])
    def remove_tag(recipe_id, tag_name):
        user_id = session.get('id')
        err = remove_tag_of_recipe(tag_name, recipe_id, user_id)
        if not err:
            return 'remove tag of recipe success', 200
        else:
            return err, 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.debug = os.getenv("DEBUG") == "true"
    app.run()

