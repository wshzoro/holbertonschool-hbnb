from app.models.users import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import repo, InMemoryRepository

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

    def create_place(self, place_data):
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id', 'amenities']
        for field in required_fields:
            if field not in place_data or not place_data[field]:
                raise ValueError(f"{field} is required")

        owner = repo.get(User, place_data['owner_id'])
        if not owner:
            raise ValueError("Invalid owner_id")

        for amenity_id in place_data['amenities']:
            if not repo.get(Amenity, amenity_id):
                raise ValueError(f"Amenity not found: {amenity_id}")

        place = Place(**place_data)
        repo.save(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        return repo.all(Place)

    def update_place(self, place_id, update_data):
        place = repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")

        for key, value in update_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        repo.save(place)
        return place

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
