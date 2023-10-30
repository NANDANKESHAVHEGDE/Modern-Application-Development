from .database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    lists = db.relationship('List', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String)
    list_desc = db.Column(db.String)
    username = db.Column(db.String, db.ForeignKey("user.username"), primary_key=True, nullable=False)
    cards = db.relationship('Card', backref='list', lazy=True, cascade="all, delete")
    users = db.relationship('User', backref='list', lazy=True)

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  
    card_name = db.Column(db.String)
    card_content = db.Column(db.String)
    card_deadline = db.Column(db.String)
    completion = db.Column(db.String)
    comp_date = db.Column(db.String)
    created_date = db.Column(db.String)
    updated_date = db.Column(db.String)
    list_id = db.Column(db.Integer, db.ForeignKey("list.list_id"), primary_key=True, nullable=False)
 
