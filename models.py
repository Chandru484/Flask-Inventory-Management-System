from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a db object without initializing it
db = SQLAlchemy()

class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return f'<Product {self.product_id}>'

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return f'<Location {self.location_id}>'

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    # Define relationships
    product = db.relationship('Product', backref='movements')
    source = db.relationship('Location', foreign_keys=[from_location], backref='outgoing_movements')
    destination = db.relationship('Location', foreign_keys=[to_location], backref='incoming_movements')
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'