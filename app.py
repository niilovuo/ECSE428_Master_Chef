from flask import Flask, render_template, request
import os
import random
from project.db import init_db_session, deinit_db_session
from project.account import add_new_account

app = Flask(__name__)

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
            return render_template("/register.html", value=err)

        # return to register page with "Success" for now
        return render_template("/register.html", value="Success")

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
    app.debug = os.getenv("DEBUG") == "true"
    app.run()
    deinit_db_session()

