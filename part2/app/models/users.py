from part2.app.models.base_model import BaseModels

class User(BaseModels):
    def __init__(self, firs_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = firs_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def register(self):
        self.save()
    
    def delete(self):
        pass


