from .base_model import BaseModels
from app import bcrypt
import uuid

class User(BaseModels):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._password = None
        self.password_hash = None
        self.is_admin = is_admin
        self.place_list = []
        self.reviews = []
        if password:
            self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self._password = password

    def verify_password(self, password):
        if not self.password_hash or not password:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def register(self):
        self.save()
    
    def delete(self):
        pass



