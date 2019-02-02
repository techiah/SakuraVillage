from sqlalchemy import Column, Integer, String, ForeignKey

from sakura_village.extensions import DB
from sakura_village.models.mixin import TimestampMixin


class User(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    login_name = Column(String(128), nullable=False)
    password = Column(String(512), nullable=False)


class Profile(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey(User.id))
    user = DB.relationship('User', backref=DB.backref('profile', uselist=False, cascade='all, delete-orphan'))

    nickname = Column(String(32), nullable=False)