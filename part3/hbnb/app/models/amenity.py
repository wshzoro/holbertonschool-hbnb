from app.models.base_model import BaseModels

class Amenity(BaseModels):
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    def delete(self):
        pass