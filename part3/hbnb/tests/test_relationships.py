from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from datetime import datetime
import uuid
import os
import sys

# Ajouter le répertoire parent au PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_relationships():
    # Créer une application Flask de test
    app = create_app('config.TestingConfig')
    with app.app_context():
        # Créer l'utilisateur
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            is_admin=False
        )
        db.session.add(user)
        
        # Créer les équipements
        amenity1 = Amenity(name="Piscine")
        amenity2 = Amenity(name="Wi-Fi")
        db.session.add_all([amenity1, amenity2])
        
        # Créer un lieu
        place = Place(
            title="Villa de Luxe",
            description="Magnifique villa avec vue sur la mer",
            price=200.0,
            latitude=43.2965,
            longitude=5.3698,
            owner_id=str(user.id)
        )
        place.amenities.extend([amenity1, amenity2])
        db.session.add(place)
        
        # Créer un avis
        review = Review(
            text="Superbe lieu, très propre et bien situé.",
            rating=5,
            user_id=str(user.id),
            place_id=str(place.id)
        )
        db.session.add(review)
        
        # Commit toutes les modifications
        db.session.commit()
        
        # Tests des relations
        print("\n=== Tests des relations ===")
        
        # 1. User → Place
        print("\n1. User → Place")
        print(f"Nombre de lieux de l'utilisateur : {len(user.places)}")
        print(f"Lieu : {user.places[0].title}")
        
        # 2. Place → User
        print("\n2. Place → User")
        print(f"Propriétaire du lieu : {place.owner.first_name} {place.owner.last_name}")
        
        # 3. Place → Review
        print("\n3. Place → Review")
        print(f"Nombre d'avis sur le lieu : {len(place.reviews)}")
        print(f"Avis : {place.reviews[0].text}")
        
        # 4. Review → Place
        print("\n4. Review → Place")
        print(f"Lieu de l'avis : {review.place.title}")
        
        # 5. User → Review
        print("\n5. User → Review")
        print(f"Nombre d'avis de l'utilisateur : {len(user.reviews)}")
        print(f"Avis : {user.reviews[0].text}")
        
        # 6. Place ↔ Amenity
        print("\n6. Place ↔ Amenity")
        print(f"Nombre d'équipements du lieu : {len(place.amenities)}")
        for amenity in place.amenities:
            print(f"- {amenity.name}")
        
        # 7. Amenity ↔ Place
        print("\n7. Amenity ↔ Place")
        print(f"Nombre de lieux avec la piscine : {len(amenity1.places)}")
        print(f"Lieu : {amenity1.places[0].title}")
        
        # 8. Vérification de l'intégrité
        print("\n8. Vérification de l'intégrité")
        print(f"ID du propriétaire du lieu : {place.owner_id}")
        print(f"ID de l'utilisateur : {user.id}")
        print(f"ID du lieu dans l'avis : {review.place_id}")
        print(f"ID du lieu : {place.id}")

if __name__ == '__main__':
    test_relationships()
