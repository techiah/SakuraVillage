from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Text

from sakura_village.extensions import DB


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class User(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    login_name = Column(String(128), nullable=False)
    password = Column(String(512), nullable=False)


class Profile(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey(User.id))
    user = DB.relationship('User', backref=DB.backref('profile', uselist=False, cascade='all, delete-orphan'))

    nickname = Column(String(32), nullable=False)


class Post(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    poster_id = Column(ForeignKey(User.id))
    poster = DB.relationship('User', backref=DB.backref('posts', uselist=True))

    title = Column(String(30), nullable=False)
    content = Column(Text(10000), nullable=False)


class Comment(DB.Model, TimestampMixin):
    id = Column(Integer, primary_key=True)

    post_id = Column(ForeignKey(Post.id))
    post = DB.relationship('Post', backref=DB.backref('comments', uselist=True))

    poster_id = Column(ForeignKey(User.id))
    poster = DB.relationship('User', backref=DB.backref('comments', uselist=True))

    content = Column(Text(5000), nullable=False)
