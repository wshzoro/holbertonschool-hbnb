from part2.app.models.base_model import BaseModels

class Amenity(BaseModels):
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    def delete(self):
        pass
