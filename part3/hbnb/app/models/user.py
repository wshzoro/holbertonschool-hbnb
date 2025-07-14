from app.models.baseclass import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    # Colonnes de base héritées de BaseModel
    # id, created_at, updated_at

    # Colonnes spécifiques à User
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    @property
    def password(self):
        """Le mot de passe n'est pas accessible directement"""
        raise AttributeError('Le mot de passe n\'est pas un attribut lisible')

    def hash_password(self, password):
        """Hacher le mot de passe avant de le stocker"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifier le mot de passe haché"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_relationships=False):
        """Convertir l'objet en dictionnaire"""
        result = super().to_dict()
        if include_relationships:
            result['places'] = [place.to_dict() for place in self.places]
            result['reviews'] = [review.to_dict() for review in self.reviews]
        return result


