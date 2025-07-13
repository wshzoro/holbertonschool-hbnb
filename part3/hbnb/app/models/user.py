from app.models.base_model import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Relations
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.password = password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



