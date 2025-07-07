from .base_model import BaseModels
from app import bcrypt

class User(BaseModels):
    def __init__(self, first_name, last_name, email, password, place_list=[], reviews=[], is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = None
        self.password_hash = None
        self.is_admin = is_admin
        self.place_list = []
        self.reviews = []

    def password_hash(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def register(self):
        self.save()
    
    def delete(self):
        pass



