from flask import Flask, render_template, request, flash
import os
import random
from project.db import init_db_session, deinit_db_session, setup_db_tables
from project.account import add_new_account

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

