from app import app
from app.models import Product
from app.forms import ProductIdForm
from flask import Flask, render_template, redirect, url_for, request, send_file
from app.utils import get_all_products_info, get_file_for_download, get_dependencies_as_string

    # two methods of obtaining data from the client
    # get : data is visible
    # post : data is hidden

@app.route("/")
def index():
    return render_template("index.html", requirements=get_dependencies_as_string())

@app.route("/extract")
def display_extract():
    form = ProductIdForm()
    return render_template("extract.html", form=form)

@app.route("/extract", methods=["POST"])
def extract():
    form = ProductIdForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        product = Product(product_id)
        product.extract_name()
        product.extract_opinions()
        product.calculate_statistics()
        product.generate_charts()
        product.save_opinions()
        product.save_info()
        return redirect(url_for('product', product_id=product_id))
    else:
        return render_template("extract.html", form=form)

@app.route("/product/<product_id>")
def product(product_id = "N/A"):
    return render_template("product.html", product_id=product_id)

@app.route("/charts/<product_id>")
def charts(product_id = "N/A"):
    return render_template("charts.html", product_id=product_id)

@app.route("/products")
def products():
    return render_template("products.html", products = get_all_products_info())
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/download/<model>/<file_format>/<product_id>")
def download_file(model, file_format, product_id):
    path, filename = get_file_for_download(model, file_format, product_id)
    return send_file(path, as_attachment=True, download_name=filename)
