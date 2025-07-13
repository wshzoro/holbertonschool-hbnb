from app.models.user import User
from app import db
from sqlalchemy.orm import Session
from .repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self, session: Session = None):
        if session is None:
            session = db.session
        super().__init__(session, User)

    def get_by_email(self, email):
        """Get a user by email address."""
        return self.session.query(User).filter_by(email=email).first()

    def get_admins(self):
        """Return all admin users."""
        return self.session.query(User).filter_by(is_admin=True).all()

