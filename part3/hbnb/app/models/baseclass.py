from app import db
import uuid
from datetime import datetime
from sqlalchemy import func

class BaseModel(db.Model):
    __abstract__ = True  # Empêche la création d'une table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_relationships=False):
        """Convertir l'objet en dictionnaire"""
        columns = [c.name for c in self.__table__.columns]
        result = {}
        for col in columns:
            value = getattr(self, col)
            if isinstance(value, datetime):
                result[col] = value.isoformat()
            else:
                result[col] = value
        return result

    def save(self):
        """Sauvegarder l'objet dans la base de données"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Supprimer l'objet de la base de données"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, obj_id):
        """Récupérer un objet par son ID"""
        return cls.query.get(obj_id)

    @classmethod
    def get_all(cls):
        """Récupérer tous les objets"""
        return cls.query.all()

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        """Récupérer un objet par attribut"""
        return cls.query.filter(getattr(cls, attr_name) == attr_value).first()

    def update(self, data):
        """Mettre à jour les attributs de l'objet"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
