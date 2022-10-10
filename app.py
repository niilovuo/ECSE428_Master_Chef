from flask import Flask, render_template
import os
import random

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("/home.html", value = random.randrange(1024))

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = os.getenv("DEBUG") == "true"
    app.run()
