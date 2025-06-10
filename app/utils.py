import os
import json
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
            os.mkdir(path)

def create_if_not_exists_multiple(paths):
    for path in paths:
        create_if_not_exists(path)

def get_all_products_info():
    if os.path.exists('./app/data/products'):
        return [
            product for product in (
                read_product_info_from_json(os.path.join('./app/data/products', file))
                for file in os.listdir('./app/data/products')
            ) if product is not None
        ]
    return None

def read_product_info_from_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="UTF-8") as json_file:
            return json.load(json_file)
    return None