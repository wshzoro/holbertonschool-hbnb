import uuid
from datetime import datetime

class BaseModels:
    def __init__(self):
        self.id = str(uuid.uiid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()
