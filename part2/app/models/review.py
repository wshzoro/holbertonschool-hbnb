from part2.app.models.base_model import BaseModels

class Reviews(BaseModels):
    def __init__(self, id, text, rating, place, user):
        super().__init__()
        self.id = id
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def delete(self):
        pass
