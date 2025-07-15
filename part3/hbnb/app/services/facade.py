from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
import bcrypt

class HBnBFacade:
    def __init__(self):
        # Initialisation des référentiels
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
        
    """ USERS """

    def create_user(self, user_data):
        """Créer un nouvel utilisateur."""
        if not self.user_repo.is_email_available(user_data['email']):
            return None

        user = User(**user_data)
        user.hash_password(user_data['password'])
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """Récupérer un utilisateur par ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Récupérer un utilisateur par email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Récupérer tous les utilisateurs."""
        return self.user_repo.get_all()

    def hash_password(self, password):
        """Hacher un mot de passe."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def update_user(self, user_id, update_data):
        """Mettre à jour un utilisateur existant."""
        if 'password' in update_data:
            user = self.get_user(user_id)
            if user:
                user.hash_password(update_data['password'])
                update_data['password_hash'] = user.password_hash
                del update_data['password']
        return self.user_repo.update(user_id, update_data)

    """ REVIEWS """

    def create_review(self, review_data):
        """Create a new review."""
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Récupérer tous les avis."""
        return self.review_repo.get_all()

    def get_reviews_by_rating(self, min_rating=1, max_rating=5):
        """Rechercher les avis par note."""
        return self.review_repo.get_reviews_by_rating(min_rating, max_rating)

    def get_reviews_by_text(self, text):
        """Rechercher les avis par texte."""
        return self.review_repo.get_reviews_by_text(text)

    def get_average_rating_for_place(self, place_id):
        """Calculer la note moyenne pour un lieu."""
        return self.review_repo.get_average_rating_for_place(place_id)

    def update_review_rating(self, review_id, new_rating):
        """Mettre à jour la note d'un avis."""
        return self.review_repo.update_rating(review_id, new_rating)

    def get_reviews_by_place(self, place_id):
        """Return all reviews for a specific place."""
        return self.review_repo.get_by_attribute('place_id', place_id)

    def get_reviews_by_user(self, user_id):
        """Return all reviews by a specific user."""
        return self.review_repo.get_by_attribute('user_id', user_id)

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        return self.review_repo.delete(review_id)
        return False

    """PLACES"""

    def create_place(self, place_data):
        """Create a new place."""
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Récupérer tous les lieux."""
        return self.place_repo.get_all()

    def get_places_by_location(self, latitude, longitude, radius=10):
        """Rechercher les lieux dans un rayon donné."""
        return self.place_repo.get_places_by_location(latitude, longitude, radius)

    def get_places_by_price_range(self, min_price, max_price):
        """Rechercher les lieux dans une fourchette de prix."""
        return self.place_repo.get_places_by_price_range(min_price, max_price)

    def get_places_by_title(self, title):
        """Rechercher les lieux par titre partiel."""
        return self.place_repo.get_places_by_title(title)

    def update_place_location(self, place_id, latitude, longitude):
        """Mettre à jour la localisation d'un lieu."""
        return self.place_repo.update_location(place_id, latitude, longitude)

    def update_place(self, place_id, update_data):
        """Update an existing place with new data."""
        return self.place_repo.update(place_id, update_data)

    """ AMENITIES """

    def create_amenity(self, amenity_data):
        """Create a new amenity if valid."""
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Missing or invalid amenity name")
        amenity = Amenity(id=amenity_data['id'], name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        """Récupérer tous les équipements."""
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        """Rechercher un équipement par nom."""
        return self.amenity_repo.get_amenity_by_name(name)

    def get_amenities_by_place(self, place_id):
        """Rechercher les équipements d'un lieu."""
        return self.amenity_repo.get_amenities_by_place(place_id)

    def get_places_with_amenity(self, amenity_id):
        """Rechercher les lieux avec un équipement."""
        return self.amenity_repo.get_places_with_amenity(amenity_id)

    def update_amenity_name(self, amenity_id, new_name):
        """Mettre à jour le nom d'un équipement."""
        return self.amenity_repo.update_name(amenity_id, new_name)

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        """Delete an amenity by ID."""
        return self.amenity_repo.delete(amenity_id)

    def update_amenity(self, amenity_id, update_data):
        """Update an existing amenity with new data."""
        return self.amenity_repo.update(amenity_id, update_data)

    """ REVIEWS """

    def create_review(self, review_data):
        """Create a new review."""
        required_fields = ['place_id', 'user_id', 'rating', 'comment']
        for field in required_fields:
            if field not in review_data or not review_data[field]:
                raise ValueError(f"{field} is required")

        place = self.place_repo.get(review_data['place_id'])
        user = self.user_repo.get(review_data['user_id'])
        
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
        