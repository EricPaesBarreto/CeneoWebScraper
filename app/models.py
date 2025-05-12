class Product:
    def __init__(self):
        pass

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
        'date_purchased': ("span.user-post__published > time:nth-child(2)", "datetime")
    }

    def __init__(self, opinion_id, author, recommendation, score, content, pros, cons, thumbs_up, thumbs_down, date_published, date_purchased):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.score = score
        self.content = content
        self.pros = pros
        self.cons = cons
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.date_published = date_published
        self.date_purchased = date_purchased

    def __str__(self):
        return "\n".join([f"{key}: {getattr(self,key)}" for key in self.selectors.keys()])

    def __repr__(self):
        return "Opinion("+", ".join([f"{key}={getattr(self,key)}" for key in self.selectors.keys()])+")"