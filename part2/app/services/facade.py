from app.models.users import User
from app.persistence.repository import repo
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.all()

    def update_user(self, user_id, update_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        return user

    def get_place(self, place_id):
        pass

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity = Amenity(name=amenity_data['name'])
        repo.save(amenity)
        return amenity.to_dict()

    def get_all_amenities(self):
        amenities = repo.all(Amenity)
        return [a.to_dict() for a in amenities]

    def get_amenity(self, amenity_id):
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return None
        return amenity.to_dict()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return None
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity.name = amenity_data['name']
        repo.save(amenity)
        return {"message": "Amenity updated successfully"}