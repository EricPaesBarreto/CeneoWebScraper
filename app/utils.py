import os
import json
import pandas as pd
from deep_translator import GoogleTranslator


# define a function to rerurn a given child selector(s) from within a given ancestor
def extract_data(ancestor, selector=None, attribute = None, multiple = False):
    if selector:
        if multiple:
            if attribute:
                return [tag[attribute].strip() for tag in ancestor.select(selector)]
            return [tag.text.strip() for tag in ancestor.select(selector)]
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except TypeError:
                return None
        try:
            return ancestor.select_one(selector).text.strip()
        except AttributeError:
            return None
    if attribute:
        return ancestor[attribute]
    return None

def translate_data(text, source = 'pl', target = 'en'):
    return GoogleTranslator(source, target).translate(text)

def create_if_not_exists(path):
    if os.path.exists(path) is not True:
            os.makedirs(path)

def create_if_not_exists_multiple(paths):
    for path in paths:
        create_if_not_exists(path)

def get_all_products_info():
    if os.path.exists('./app/data/products'):
        products_info = [
            product for product in (
                read_product_info_from_json(os.path.join('./app/data/products', file))
                for file in os.listdir('./app/data/products')
             ) if product is not None
        ]
    if len(products_info) > 0:
        return products_info
    # if there are no products
    return None

def read_product_info_from_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="UTF-8") as json_file:
            return json.load(json_file)
    return None

def json_to_data_frame(path):
    with open(path, 'r', encoding="UTF-8") as json_file:
        return pd.json_normalize(json.load(json_file))
    
def get_file_for_download(product_id, file_format):
    # determine current path to prevent errors
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "data")

    # folder for converted files
    converted_path = os.path.join(data_path, "converted_files")
    csv_path = os.path.join(converted_path, "csv")
    xlsx_path = os.path.join(converted_path, "xlsx")

    # create folders if missing
    create_if_not_exists_multiple([data_path, converted_path, csv_path, xlsx_path])

    # default json path
    json_path = os.path.join(data_path, "products", f"{product_id}.json")

    # change based on file_type
    match file_format:
        case "json":
            return json_path, f"{product_id}.json"
        case "csv":
            csv_file = os.path.join(csv_path, f"{product_id}.csv")
            data = read_product_info_from_json(json_path)
            pd.DataFrame([data]).to_csv(csv_file, index=False)
            return csv_file, f"{product_id}.csv"
        case "xlsx":
            xlsx_file = os.path.join(xlsx_path, f"{product_id}.xlsx")
            data = read_product_info_from_json(json_path)
            pd.DataFrame([data]).to_excel(xlsx_file, index=False)
            return xlsx_file, f"{product_id}.xlsx"