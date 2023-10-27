from .database import db
from datetime import datetime


class User(db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    email_id = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)

class Manager(db.Model):

    __tablename__ = 'manager'

    manager_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    manager_name = db.Column(db.String, unique=True)
    email_id = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)

class InventoryProduct(db.Model):

    __tablename__ = 'products'

    Product_ID = db.Column(db.String(50), primary_key=True)
    Category_ID = db.Column(db.String(50), nullable=False)
    Category_Name = db.Column(db.String(100),nullable=False)
    Product_Name = db.Column(db.String(100), nullable=False)
    Manufacture_date = db.Column(db.Date, nullable=False)
    Expiry_date = db.Column(db.Date, nullable=False)
    Price_per_unit = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    Stocks = db.Column(db.Integer, nullable=False)
    Unit = db.Column(db.String(50), nullable=True)

class Cart(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.Product_ID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Order(db.Model):

    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.Product_ID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
