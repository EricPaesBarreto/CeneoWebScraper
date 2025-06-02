# external
import os
import json
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
# internal
from config import headers
from utils import extract_data, translate_data

class Product:
    def __init__(self, product_id, product_name="", opinions=[], product_statistics={}):
        self.product_id = product_id
        self.product_name()
        self.opinions = opinions
        self.product_statistics = product_statistics
    
    def __str__(self):
        return f"product_id: {self.product_id}, product_name: {self.product_name}\nproduct_statistics:"+json.dumps(self.product_statistics, indent=4,ensure_ascii=False)+"\nopinions:"+"\n\n".join([str(opinion) for opinion in self.opinions])

    def __repr__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions=["+", ".join(repr(opinion for opinion in self.opinions))+f"], product_statistics={self.product_statistics})"

    def get_link(self):
        return f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
    
    def extract_name(self):
        response = requests.get(self.get_link(), headers = headers)
        page_dom = BeautifulSoup(response.text, 'html.parser')
        self.product_name = page_dom.select_one("h1").text()

    def opinions_to_dict(self):
        return [opinion.to_dict() for opinion in self.opinions]

    def calculate_statistics(self):
        opinions = pd.DataFrame.from_dict(self.opinions_to_dict())
        self.product_statistics["opinions_count"] = opinions.shape[0]
        self.product_statistics["pros_count"] = sum(opinions.pros_pl.astype(bool)) # converts the list into a bool [empty]/[not-empty], the sum counts trues a 1s and falses as 0s
        self.product_statistics["cons_count"] = sum(opinions.cons_pl.astype(bool))
        self.product_statistics["pros_cons_count"] = opinions.apply(lambda opinion: bool(opinion.pros_pl) and bool(opinion.cons_pl), axis=1).sum() 
        self.product_statistics["average_score"] = opinions.score.mean()
        self.product_statistics["pros"] = opinions.pros_en.explode().value_counts()
        self.product_statistics["cons"] = opinions.pros_en.explode().value_counts()
        self.product_statistics["recommendations"] = opinions.recommendation.value_counts(dropna=False).reindex([True, False, None], fill_value=0)
        self.product_statistics["scores"] = opinions.score.value_counts().reindex(list(np.arange(0.5,5.5,0.5)), fill_value=0)

    def generate_charts(self):
        if not os.path.exists("./app/static/opinions"):
            os.mkdir("./pie_charts")
        if not os.path.exists("./app/static/bar_charts"):
            os.mkdir("./bar_charts")

        self.product_statistics["recommendations"].plot.pie(
            label = "",
            labels = ["Recommend", "Not recommend", "No opinion"], # same order as stated in the reindex order statement above
            colors = ["forestgreen", "crimson", "steelblue"], # colours
            autopct = lambda r: f"{r:.1f}%" if r > 0 else "" # function that returns a percentage value only if greate than 0%, (exclude) from chart
        )
        plt.title(f"recommendations for product {self.product_id}")
        plt.savefig(f"./pie_charts/{self.product_id}.png")

        ax = self.product_statistics["scores"].plot.bar(
            color = ["forestgreen" if s > 3.5 else "crimson" if s < 3 else "steelblue" for s in self.product_statistics["scores"].index]
        )
        plt.bar_label(container=ax.containers[0])
        plt.xlabel("Score")
        plt.ylabel("Number of opinions")
        no_opinions = len(self.opinions)
        plt.title("Number of opinions about {self.product_id} by their respective scores.\nTotal number of opinions: {no_opinions}")
        plt.xticks(rotation=0)
        plt.savefig(f"./bar_charts/{self.product_id}.png")

        plt.close()

    def extract_opinion():
        all_opinions = []
        while url is not None:
            response = requests.get(url, headers = headers)
            if response.status_code == 200:
                page_doc = BeautifulSoup(response.text, 'html.parser')
                opinions = page_doc.select("div.js_product-review:not(.user-post--highlight)")
                for opinion in opinions:
                    single_opinion = Opinion()
                    single_opinion.extract(opinion)

                    # optional translation
                    try:
                        single_opinion['content_en'] = translate_data(single_opinion['content_pl'])
                    except Exception:
                        single_opinion['content_en'] = None
                    try:
                        single_opinion['pros_en'] = [translate_data(pro_pl) for pro_pl in single_opinion['pros_pl']]
                    except Exception:
                        single_opinion['pros_en'] = None
                    try:
                        single_opinion['cons_en'] = [translate_data(con_pl) for con_pl in single_opinion['cons_pl']]
                    except Exception:
                        single_opinion['cons_en'] = None
                    
                    single_opinion['recommendation'] = True if single_opinion['recommendation'] == "Polecam" else False if single_opinion['recommendation']  == "Nie polecam" else None
                    single_opinion['score'] = float(single_opinion['score'].split('/')[0].replace(",","."))
                    # single_opinion['date_published'] = datetime.datetime.fromisoformat(single_opinion['date_published'])
                    # single_opinion['date_purchased'] = datetime.datetime.fromisoformat(single_opinion['date_purchased']) if single_opinion['date_purchased'] else None
                    single_opinion['thumbs_up'] = int(single_opinion['thumbs_up'])
                    single_opinion['thumbs__down'] = int(single_opinion['thumbs_down'])

                    all_opinions.append(single_opinion)
                try:
                    url = "https://www.ceneo.pl"+page_doc.select_one("a.pagination__next")["href"]
                except TypeError:
                    url = None


class Opinion:
    selectors = {
        'opinion_id': (None, "data-entry-id"),
        'author': ("span.user-post__author-name",),
        'recommendation': ("span.user-post__author-recomendation > em",),
        'score': ("span.user-post__score-count",),
        'content_pl': ("div.user-post__text",),
        'pros_pl': ("div.review-feature__item--positive", None, True),
        'cons_pl': ("div.review-feature__item--negative", None, True),
        'thumbs_up': ("button.vote-yes", "data-total-vote",),
        'thumbs_down': ("button.vote-no", "data-total-vote",),
        'date_published': ("span.user-post__published > time:nth-child(1)", "datetime"),
        'date_purchased': ("span.user-post__published > time:nth-child(2)", "datetime"),
        'content_en': "",
        'pros_en' : (),
        'cons_en' : ()
    }

    def __init__(self, opinion_id="", author="", recommendation=False, score=0, content_pl="", pros_pl=[], cons_pl=[], thumbs_up=0, thumbs_down=0, date_published=None, date_purchased=None, content_en="", pros_en=[], cons_en=[]):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.score = score
        self.content_pl = content_pl
        self.pros_pl = pros_pl
        self.cons_pl = cons_pl
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.date_published = date_published
        self.date_purchased = date_purchased
        self.content_en = content_en
        self.pros_en = pros_en
        self.cons_en = cons_en

    def __str__(self):
        return "\n".join([f"{key}: {getattr(self,key)}" for key in self.selectors.keys()])

    def __repr__(self):
        return "Opinion("+", ".join([f"{key}={getattr(self,key)}" for key in self.selectors.keys()])+")"
    
    def convert_to_dictionary(self):
            return {key: getattr(self,key) for key in self.selectors.keys()}

    def extract(self, opinion):
        for key, values in self.selecors.items():
            setattr(self, key, extract_data(opinion, *values))
    
    def translate(self):
        self.content_en = translate_data(self.content_pl)
        self.pros_en = [translate_data(pros) for pros in self.pros_pl]
        self.cons_en = [translate_data(cons) for cons in self.cons_pl]
        