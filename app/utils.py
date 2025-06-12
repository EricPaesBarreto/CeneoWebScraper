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
    try:
        GoogleTranslator(source, target).translate(text)
    except Exception:
        return "Translation Error"
    # sometimes the number of requests maxes out or some other issue occurs

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
                read_product_info_from_json(path=os.path.join('./app/data/products', file))
                for file in os.listdir('./app/data/products')
             ) if product is not None
        ]
    if len(products_info) > 0:
        return products_info
    # if there are no products
    return None

def read_product_info_from_json(path=None, product_id=None):
    if path:
        if os.path.exists(path):
            with open(path, "r", encoding="UTF-8") as json_file:
                return json.load(json_file)
    elif product_id:
        # path = None, set path
        path = os.path.join(get_base_path(), 'products', product_id)

        if os.path.exists(path):
            with open(path, "r", encoding="UTF-8") as json_file:
                return json.load(json_file)

    # None, None
    return None

def json_to_data_frame(path):
    with open(path, 'r', encoding="UTF-8") as json_file:
        return pd.json_normalize(json.load(json_file))
    
def get_base_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))
    
def get_file_for_download( model, file_format, product_id):
    # product_id is the id, model is either 'product' or 'opinions', file format is either 'json', 'csv', or 'xlsx'

    # determine current path to prevent errors
    base_path = get_base_path()
    data_path = os.path.join(base_path, "data")

    # folder for converted files
    converted_path = os.path.join(data_path, "converted_files", model)
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
            data = read_product_info_from_json(path=json_path)
            pd.DataFrame([data]).to_csv(csv_file, index=False)
            return csv_file, f"{product_id}.csv"
        case "xlsx":
            xlsx_file = os.path.join(xlsx_path, f"{product_id}.xlsx")
            data = read_product_info_from_json(path=json_path)
            pd.DataFrame([data]).to_excel(xlsx_file, index=False)
            return xlsx_file, f"{product_id}.xlsx"
        
def get_dependencies_as_string():
    root_path = os.path.join(get_base_path(), os.pardir)
    requirements_path = os.path.join(root_path, 'requirements.txt')
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='UTF-8') as requirements:
            return ', '.join([r.split('==')[0] for r in requirements.readlines()])
    else:
        return ['Requirements not found.']

def get_all_opinions_info(product_id):
    # get the path of the opinions for the product
    base_path = os.path.join(get_base_path(), 'opinions')

    # get the path of the opinion
    path = os.path.join(base_path, product_id,'.json')

    opinions_info = read_opinion_info_from_json(path)
    if opinions_info:
        if len(opinions_info) > 0:
            return opinions_info
    # if there are no opinions
    return None

def read_opinion_info_from_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="UTF-8") as json_file:
            return json.load(json_file)
    return None