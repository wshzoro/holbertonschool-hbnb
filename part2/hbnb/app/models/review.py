from app.models.base_model import BaseModels


class Review(BaseModels):
    def __init__(self, id, text, rating, user_id, place_id):
        super().__init__()
        self.id = id
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def delete(self):
        pass

