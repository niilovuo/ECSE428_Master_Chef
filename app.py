from flask import Flask, render_template, request, flash
import os
import random
from project.db import init_db_session, deinit_db_session, setup_db_tables
from project.account import add_new_account
from project.tag_query import get_all_tags
from project.recipe_query import search_recipes_by_filter, search_recipe_by_id

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

@app.route("/api/search")
def api_search():
    try:
        title = request.args.get("q", type=str)
        start = request.args.get("start", 0, type=int)
        tags = request.args.getlist("tags[]", type=str)
    except:
        return "Invalid request parameters", 400

    (recipes, err) = search_recipes_by_filter(title, tags, start)
    if recipes is None:
        return err, 400

    return recipes

@app.route("/api/tags")
def api_list_tags():
    return get_all_tags()

@app.route("/api/recipes/<int:id>")
def api_lookup_recipe(id):
    recipe = search_recipe_by_id(id)
    if recipe is not None:
        return "Invalid recipe id", 404

    return recipe


if __name__ == "__main__":
    pg_user = os.getenv("POSTGRES_USER", "postgres")
    db_args = {
        "password": os.getenv("POSTGRES_PASSWORD"),
        "user": pg_user,
        "dbname": os.getenv("POSTGRES_DB", pg_user),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", 5432)
    }

    init_db_session(**db_args)
    setup_db_tables()

    app.debug = os.getenv("DEBUG") == "true"
    app.run()
    deinit_db_session()

