from app.models.base_model import BaseModels

class Place(BaseModels):
    def __init__(self, name, description, price, longitude, latitude, owner_id, amenities, reviews):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.longitude = longitude
        self.latitude = latitude
        self.owner_id = owner_id
        self.reviews = reviews
        self.amenities = amenities

    def create(self):
        self.save()
    
    def delete(self):
        pass
