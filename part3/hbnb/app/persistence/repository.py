from abc import ABC, abstractmethod
from app import db
from sqlalchemy.exc import SQLAlchemyError

class Repository(ABC):
    @abstractmethod
    def add(self, obj): pass

    @abstractmethod
    def get(self, obj_id): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def update(self, obj_id, data): pass

    @abstractmethod
    def delete(self, obj_id): pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value): pass


class SQLAlchemyRepository(Repository):
    def __init__(self, session, model_class):
        self.session = session
        self.model_class = model_class

    def add(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
            return obj
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get(self, obj_id):
        return self.session.query(self.model_class).get(obj_id)

    def get_all(self):
        return self.session.query(self.model_class).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    setattr(obj, key, value)
                self.session.commit()
                return obj
            except SQLAlchemyError as e:
                self.session.rollback()
                raise
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            try:
                self.session.delete(obj)
                self.session.commit()
                return True
            except SQLAlchemyError as e:
                self.session.rollback()
                raise
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.session.query(self.model_class).filter(getattr(self.model_class, attr_name) == attr_value).first()
