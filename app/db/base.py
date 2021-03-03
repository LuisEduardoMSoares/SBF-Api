import sqlalchemy as db
from sqlalchemy import func

from sqlalchemy.orm import Session


# Base Mixin object.
class BaseMixin():
    __mapper_args__ = {'always_refresh': True}

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())

    @property
    def metadata(self):
        return self

    def insert(self, session: Session) -> object:
        """
        Use only for insert operation
        """
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except:
            session.rollback()
            raise

    def update(self, session: Session, **kwargs) -> None:
        """
        User only for update operation
        """
        try:
            # set the new values
            for key, value in kwargs.items():
                setattr(self, key, value)
            # commit the modifications
            session.commit()
        except:
            session.rollback()
            raise

    def delete(self, session: Session) -> None:
        """
        User only for delete operation
        """
        try:
            session.delete(self)
            session.commit()
        except:
            session.rollback()
            raise