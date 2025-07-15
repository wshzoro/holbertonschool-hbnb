from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(db.session, Review)

    def get_reviews_by_rating(self, min_rating=1, max_rating=5):
        """Rechercher les avis par note"""
        return self.session.query(Review).filter(
            Review.rating.between(min_rating, max_rating)
        ).all()

    def get_reviews_by_text(self, text):
        """Rechercher les avis par texte"""
        return self.session.query(Review).filter(
            Review.text.ilike(f'%{text}%')
        ).all()

    def get_average_rating_for_place(self, place_id):
        """Calculer la note moyenne pour un lieu"""
        result = self.session.query(
            db.func.avg(Review.rating).label('average_rating')
        ).filter_by(place_id=place_id).first()
        return result.average_rating if result else None

    def update_rating(self, review_id, new_rating):
        """Mettre à jour la note d'un avis"""
        if not 1 <= new_rating <= 5:
            raise ValueError("La note doit être entre 1 et 5")
        
        try:
            review = self.get(review_id)
            if review:
                review.rating = new_rating
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
