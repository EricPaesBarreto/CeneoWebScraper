from app import app
from flask import Flask, render_template
    # two methods of obtaining data from the client
    # get : data is hidden
    # post : data is visible

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract/")
def extract():
    return render_template("extract.html")

@app.route("/product/<product_id>")
def product(product_id = "N/A"):
    return render_template("product.html", product_id=product_id)

@app.route("/charts/<product_id>")
def charts(product_id = "N/A"):
    return render_template("charts.html", product_id=product_id)

@app.route("/products")
def products():
    return render_template("products.html")
    
@app.route("/about")
def about():
    return render_template("about.html")