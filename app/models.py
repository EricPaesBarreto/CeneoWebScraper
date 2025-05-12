class Product:
    def __init__(self):
        pass

class Opinion:
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