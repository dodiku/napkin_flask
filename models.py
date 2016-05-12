from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('group.id'))
    group = relationship(Group, backref=backref('posts', uselist=True))
    url = db.Column(db.String())
    text = db.Column(db.String())
