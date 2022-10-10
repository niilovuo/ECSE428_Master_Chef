from flask import Flask, render_template
import os
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("/home.html", value = random.randrange(1024))


if __name__ == "__main__":
    app.debug = os.getenv("DEBUG") == "true"
    app.run()
