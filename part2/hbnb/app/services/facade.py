from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import repo, InMemoryRepository


class HBnBFacade:
    """Main facade to manage business logic for users, places, reviews, and amenities."""

    def __init__(self):
        # In-memory repositories (can be swapped with persistent ones)
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """ USERS """

    def create_user(self, user_data):
        """Create a new user and add it to the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Return all users."""
        return self.user_repo.all()

    def update_user(self, user_id, update_data):
        """Update an existing user with new data."""
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        return user

        """ PLACES """

    def create_place(self, place_data):
        """Create a new place after validating required fields and related entities."""
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
        """Retrieve a place by ID."""
        place = repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """Return all places."""
        return repo.all(Place)

    def update_place(self, place_id, update_data):
        """Update an existing place with new data."""
        place = repo.get(Place, place_id)
        if not place:
            raise ValueError("Place not found")

        for key, value in update_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        repo.save(place)
        return place

        """ AMENITIES """

    def create_amenity(self, amenity_data):
        """Create a new amenity if valid."""
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity = Amenity(name=amenity_data['name'])
        repo.save(amenity)
        return amenity.to_dict()

    def get_all_amenities(self):
        """Return all amenities."""
        amenities = repo.all(Amenity)
        return [a.to_dict() for a in amenities]

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return None
        return amenity.to_dict()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity's name."""
        amenity = repo.get(Amenity, amenity_id)
        if not amenity:
            return None
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity.name = amenity_data['name']
        repo.save(amenity)
        return {"message": "Amenity updated successfully"}
    
    """ REVIEWS """

    def create_review(self, review_data):
        """Create a new review after validating required fields."""
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        if not all(field in review_data for field in required_fields):
            raise ValueError("Missing fields in review data")

        review = Review(
            id=review_data.get('id'),
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.all()

    def update_review(self, review_id, update_data):
        """Update an existing review."""
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in update_data.items():
            setattr(review, key, value)
        return review

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.get_review(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
