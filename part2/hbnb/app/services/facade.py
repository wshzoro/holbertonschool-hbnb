import uuid
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
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """Update an existing user with new data."""
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        return user

    """ REVIEWS """

    def create_review(self, review_data):
        """Create a new review."""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Return all reviews for a specific place."""
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def get_reviews_by_user(self, user_id):
        """Return all reviews by a specific user."""
        return [review for review in self.review_repo.get_all() if review.user_id == user_id]

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id")

        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity)

        place = Place(
            name=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            longitude=place_data['longitude'],
            latitude=place_data['latitude'],
            owner_id=owner_id,
            amenities=amenities,
            reviews=[]
        )
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """Return all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """Update an existing place with new data."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        for key, value in update_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.place_repo.save(place)
        return place

    """ AMENITIES """

    def create_amenity(self, amenity_data):
        """Create a new amenity if valid."""
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity = Amenity(id=amenity_data['id'], name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        """Return all amenities."""
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity with new data."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity.name = amenity_data['name']
        return amenity

    """ REVIEWS """

    def create_review(self, review_data):
        """Create a new review."""
        required_fields = ['place_id', 'user_id', 'rating', 'comment']
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"{field} is required")

        place = repo.get(Place, review_data['place_id'])
        user = repo.get(User, review_data['user_id'])
        
        if not place:
            raise ValueError("Invalid place_id")
        if not user:
            raise ValueError("Invalid user_id")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_reviews_for_place(self, place_id):
        """Get all reviews for a specific place."""
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, update_data):
        """Update an existing review."""
        review = self.get_review(review_id)
        if not review:
            return None

        for key, value in update_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        
        return review

    def delete_review(self, review_id):
        """Delete a review by ID."""
        return self.review_repo.delete(review_id)