from random import randint
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.inspection import inspect


class ModelBase(object):
    __exclude__ = []

    def serialize(self):
        attrs = [a for a in inspect(self).attrs.keys() if a not in self.__class__.__exclude__]
        return {c: getattr(self, c) for c in attrs}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Group(db.Model, ModelBase):
    __tablename__ = 'group'
    __exclude__ = ['id']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)

    @staticmethod
    def generate_name():
        for i in range(1, 10):
            name = 'random-name-{}'.format(randint(1000, 9999))
            if not Group.query.filter_by(name=name).first():
                return name


    @staticmethod
    def get_or_create(name):
        group = Group.query.filter_by(name=name).first()
        if not group:
            group = Group(name=name)
            db.session.add(group)
            db.session.commit()

        return group

    def serialize(self):
        d = super(Group, self).serialize()
        d['posts'] = [p.serialize() for p in d['posts']]
        return d

    def add_post(self, url, text):
        post = Post(group=self, url=url, text=text)
        db.session.add(post)
        db.session.commit()


class Post(db.Model, ModelBase):
    __tablename__ = 'post'
    __exclude__ = ['id', 'group']

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('group.id'))
    group = relationship(Group, backref=backref('posts', uselist=True))
    url = db.Column(db.String())
    text = db.Column(db.String())
