from flask import render_template
from app import app

    # two methods of obtaining data from the client
    # get : data is hidden
    # post : data is visible

@app.route("/")
@app.route("/<name>") # get
def index(name="N/A"):
    return render_template("index.html", name=name)

@app.route("/product/<product_id>")
def product(product_id="N/A"):
    return render_template("index.html", product_id=product_id)
