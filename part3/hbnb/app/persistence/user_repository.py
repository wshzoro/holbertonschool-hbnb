from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(db.session, User)

    def get_user_by_email(self, email):
        """Récupérer un utilisateur par email"""
        return self.session.query(User).filter_by(email=email).first()

    def get_users_by_name(self, first_name=None, last_name=None):
        """Rechercher des utilisateurs par nom"""
        query = self.session.query(User)
        if first_name:
            query = query.filter(User.first_name.ilike(f'%{first_name}%'))
        if last_name:
            query = query.filter(User.last_name.ilike(f'%{last_name}%'))
        return query.all()

    def get_admins(self):
        """Récupérer tous les administrateurs"""
        return self.session.query(User).filter_by(is_admin=True).all()

    def is_email_available(self, email, user_id=None):
        """Vérifier si un email est disponible"""
        query = self.session.query(User).filter_by(email=email)
        if user_id:
            query = query.filter(User.id != user_id)
        return not query.first()

    def update_password(self, user_id, new_password):
        """Mettre à jour le mot de passe d'un utilisateur"""
        try:
            user = self.get(user_id)
            if user:
                user.hash_password(new_password)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def update_admin_status(self, user_id, is_admin):
        """Mettre à jour le statut administrateur d'un utilisateur"""
        try:
            user = self.get(user_id)
            if user:
                user.is_admin = is_admin
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise
