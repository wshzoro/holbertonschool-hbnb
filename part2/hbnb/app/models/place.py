from app.models.base_model import BaseModels

class Place(BaseModels):
    def __init__(self, name, description, price, longitude, latitude, owner):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.longitude = longitude
        self.latitude = latitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def create(self):
        self.save()
    
    def delete(self):
        pass
