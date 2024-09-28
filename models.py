
##models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    unit = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    items = db.relationship('Item', backref='person', lazy=True)

class ItemSpec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    asset_number = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    items = db.relationship('Item', backref='item_spec', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    item_spec_id = db.Column(db.Integer, db.ForeignKey('item_spec.id'), nullable=False)
    deliverer = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    date_out = db.Column(db.String(20))
    time_out = db.Column(db.String(20))
    date_in = db.Column(db.String(20), nullable=True)
    time_in = db.Column(db.String(20), nullable=True)
